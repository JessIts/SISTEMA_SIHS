from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import MANAGER_ROLES
from app.core.exceptions import ForbiddenException, NotFoundException
from app.models.competencia import Competencia
from app.models.ficha import Ficha, ficha_aprendiz
from app.models.ficha_trimestre import FichaTrimestre
from app.models.horario import Horario
from app.models.programa import Programa
from app.models.resultado_aprendizaje import ResultadoAprendizaje
from app.models.roles import UserRole
from app.models.trimestre import Trimestre
from app.models.enums import EstadoTrimestre
from app.models.user import User
from app.repositories.ficha_trimestre_repository import FichaTrimestreRepository
from app.repositories.horario_repository import HorarioRepository
from app.services.horario_service import HorarioService


class MiService:
    """
    Información del usuario autenticado:
      - aprendiz   -> sus fichas (por ficha_aprendiz)
      - instructor -> las fichas donde dicta clases (por horarios)
    Nunca devuelve datos de otras fichas ni de otras personas.
    """

    def __init__(self, db: Session):
        self.db = db
        self.horario_service = HorarioService(db)

    # ------------------------------------------------------------------
    # Fichas y programas
    # ------------------------------------------------------------------
    def get_mis_fichas(self, user: User) -> list[dict]:
        fichas = self._fichas_de(user)

        resultado = []

        for ficha in fichas:
            programaciones = [
                ft for ft in ficha.fichas_trimestre
                if ft.is_active and self._puede_ver_programacion(user, ft)
            ]

            programaciones.sort(
                key=lambda ft: (ft.trimestre.anio, ft.trimestre.numero),
                reverse=True,
            )

            resultado.append({
                "uuid": ficha.uuid,
                "codigo": ficha.codigo,
                "modalidad": ficha.modalidad,
                "estado": ficha.estado,
                "fecha_inicio": ficha.fecha_inicio,
                "fecha_fin": ficha.fecha_fin,
                "jornada": ficha.jornada,
                "programa": ficha.programa,
                "programaciones": programaciones,
            })

        return resultado

    def get_mis_programas(self, user: User) -> list[dict]:
        programas: dict[int, Programa] = {}

        for ficha in self._fichas_de(user):
            programas[ficha.programa_id] = ficha.programa

        resultado = []

        for programa in sorted(programas.values(), key=lambda p: p.nombre):
            competencias = self.db.scalars(
                select(Competencia)
                .where(
                    Competencia.programa_id == programa.id,
                    Competencia.is_active.is_(True),
                )
                .order_by(Competencia.codigo)
            ).unique().all()

            resultado.append({
                "uuid": programa.uuid,
                "codigo": programa.codigo,
                "nombre": programa.nombre,
                "nivel": programa.nivel,
                "coordinacion": programa.coordinacion,
                "competencias": [
                    {
                        "uuid": competencia.uuid,
                        "codigo": competencia.codigo,
                        "descripcion": competencia.descripcion,
                        "resultados": sorted(
                            (r for r in competencia.resultados if r.is_active),
                            key=self._orden_codigo,
                        ),
                    }
                    for competencia in competencias
                ],
            })

        return resultado

    # ------------------------------------------------------------------
    # Horarios
    # ------------------------------------------------------------------
    def get_horario_ficha(self, user: User, ficha_trimestre_uuid: UUID) -> dict:
        ficha_trimestre = FichaTrimestreRepository(self.db).get_by_uuid(
            ficha_trimestre_uuid,
            include_inactive=False,
        )

        if not ficha_trimestre:
            raise NotFoundException("Horario no encontrado.")

        if user.role not in MANAGER_ROLES and not self._puede_ver_programacion(user, ficha_trimestre):
            raise ForbiddenException("No tienes acceso al horario de esta ficha.")

        return self.horario_service.get_grilla(ficha_trimestre_uuid)

    def get_mi_agenda(self, user: User, trimestre_uuid: UUID | None) -> dict:
        dias, franjas = self.horario_service.get_calendario()

        vacia = {
            "trimestre": None,
            "trimestres": [],
            "horas_programadas": 0,
            "total_clases": 0,
            "dias": dias,
            "jornadas": [],
        }

        if user.role != UserRole.INSTRUCTOR:
            return vacia

        trimestres = list(
            self.db.scalars(
                select(Trimestre)
                .join(Horario, Horario.trimestre_id == Trimestre.id)
                .where(Horario.instructor_id == user.id)
                .distinct()
                .order_by(Trimestre.anio.desc(), Trimestre.numero.desc())
            ).all()
        )

        if not trimestres:
            return vacia

        if trimestre_uuid:
            seleccionado = next((t for t in trimestres if t.uuid == trimestre_uuid), None)

            if not seleccionado:
                raise NotFoundException("No tienes clases en ese trimestre.")
        else:
            seleccionado = next(
                (t for t in trimestres if t.estado == EstadoTrimestre.ACTIVO),
                trimestres[0],
            )

        casillas = list(
            self.db.scalars(
                select(Horario).where(
                    Horario.instructor_id == user.id,
                    Horario.trimestre_id == seleccionado.id,
                )
            ).unique().all()
        )

        return {
            "trimestre": seleccionado,
            "trimestres": trimestres,
            "horas_programadas": round(
                sum(HorarioService.duracion_horas(h.franja) for h in casillas), 2
            ),
            "total_clases": len(casillas),
            "dias": dias,
            "jornadas": HorarioService.build_jornadas(dias, franjas, casillas, self._clase_agenda),
        }

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def _fichas_de(self, user: User) -> list[Ficha]:
        if user.role == UserRole.APRENDIZ:
            statement = (
                select(Ficha)
                .join(ficha_aprendiz, ficha_aprendiz.c.ficha_id == Ficha.id)
                .where(ficha_aprendiz.c.user_id == user.id)
            )
        elif user.role == UserRole.INSTRUCTOR:
            statement = (
                select(Ficha)
                .join(FichaTrimestre, FichaTrimestre.ficha_id == Ficha.id)
                .join(Horario, Horario.ficha_trimestre_id == FichaTrimestre.id)
                .where(Horario.instructor_id == user.id)
            )
        else:
            return []

        statement = (
            statement
            .where(Ficha.is_active.is_(True))
            .distinct()
            .order_by(Ficha.codigo)
        )

        return list(self.db.scalars(statement).unique().all())

    def _puede_ver_programacion(self, user: User, ficha_trimestre: FichaTrimestre) -> bool:
        if user.role == UserRole.APRENDIZ:
            return any(a.id == user.id for a in ficha_trimestre.ficha.aprendices)

        if user.role == UserRole.INSTRUCTOR:
            return HorarioRepository(self.db).find_conflict(
                Horario.ficha_trimestre_id == ficha_trimestre.id,
                Horario.instructor_id == user.id,
            ) is not None

        return False

    @staticmethod
    def _orden_codigo(resultado: ResultadoAprendizaje):
        codigo = resultado.codigo
        return (0, int(codigo)) if codigo.isdigit() else (1, codigo)

    @staticmethod
    def _clase_agenda(horario: Horario) -> dict:
        return {
            "horario_uuid": horario.uuid,
            "ficha": horario.ficha_trimestre.ficha.codigo,
            "ficha_trimestre_uuid": horario.ficha_trimestre.uuid,
            "tematica": f"{horario.resultado.codigo}. {horario.resultado.descripcion}",
            "resultado_codigo": horario.resultado.codigo,
            "modalidad": horario.modalidad,
            "ambiente": HorarioService.ambiente_texto(horario),
        }
