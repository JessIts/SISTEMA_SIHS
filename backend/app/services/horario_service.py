from collections import defaultdict
from uuid import UUID

from sqlalchemy import func, select

from app.common.pagination import build_page
from app.core.exceptions import NotFoundException, ValidationException, ConflictException
from app.models.ambiente import Ambiente
from app.models.dia_semana import DiaSemana
from app.models.enums import ModalidadClase
from app.models.ficha import ficha_aprendiz
from app.models.ficha_trimestre import FichaTrimestre
from app.models.franja_horaria import FranjaHoraria
from app.models.horario import Horario
from app.models.resultado_aprendizaje import ResultadoAprendizaje
from app.models.roles import UserRole
from app.models.trimestre import Trimestre
from app.models.user import User
from app.repositories.ambiente_repository import AmbienteRepository
from app.repositories.dia_semana_repository import DiaSemanaRepository
from app.repositories.ficha_trimestre_repository import FichaTrimestreRepository
from app.repositories.franja_horaria_repository import FranjaHorariaRepository
from app.repositories.horario_repository import HorarioRepository
from app.repositories.resultado_aprendizaje_repository import ResultadoAprendizajeRepository
from app.repositories.user_repository import UserRepository
from app.schemas.horario import HorarioCreate, HorarioUpdate
from app.services.base_service import BaseService


class HorarioService(BaseService[Horario]):
    """
    Cada horario es una CASILLA: (ficha+trimestre) x día x franja.

    Antes de guardar valida, con mensajes claros:
      - presencial => ambiente obligatorio ; sincrónico => sin ambiente
      - el instructor tiene rol instructor
      - la temática pertenece al programa de la ficha
      - no hay choques de ficha, instructor ni ambiente
    Y la base de datos vuelve a exigir las mismas reglas (constraints).
    """

    repository_class = HorarioRepository
    entity_label = "horario"

    constraint_messages = {
        "uq_horarios_ficha_celda": "La ficha ya tiene una clase en ese día y franja.",
        "uq_horarios_instructor_celda": "El instructor ya tiene una clase en ese día y franja.",
        "uq_horarios_ambiente_celda": "El ambiente ya está ocupado en ese día y franja.",
        "ck_horarios_ambiente_modalidad": "Una clase presencial requiere ambiente y una sincrónica no debe tenerlo.",
        "fk_horarios_ficha_trimestre": "El trimestre no corresponde a la programación de la ficha.",
    }

    # ------------------------------------------------------------------
    # Lectura
    # ------------------------------------------------------------------
    def get(self, entity_uuid: UUID) -> Horario:
        # Los horarios se eliminan físicamente: se buscan sin filtrar is_active
        entity = self.repository.get_by_uuid(entity_uuid, include_inactive=True)

        if not entity:
            raise NotFoundException("Horario no encontrado.")

        return entity

    def build_conditions(
        self,
        ficha_trimestre_uuid: UUID | None = None,
        trimestre_uuid: UUID | None = None,
        instructor_uuid: UUID | None = None,
        ambiente_uuid: UUID | None = None,
        dia_uuid: UUID | None = None,
    ) -> list:
        conditions = []

        if ficha_trimestre_uuid:
            conditions.append(
                Horario.ficha_trimestre.has(FichaTrimestre.uuid == ficha_trimestre_uuid)
            )

        if trimestre_uuid:
            conditions.append(Horario.trimestre.has(Trimestre.uuid == trimestre_uuid))

        if instructor_uuid:
            conditions.append(Horario.instructor.has(User.uuid == instructor_uuid))

        if ambiente_uuid:
            conditions.append(Horario.ambiente.has(Ambiente.uuid == ambiente_uuid))

        if dia_uuid:
            conditions.append(Horario.dia.has(DiaSemana.uuid == dia_uuid))

        return conditions

    def get_all(self, page: int, limit: int, conditions: list | None = None) -> dict:
        items, total = self.repository.get_all(
            page=page,
            limit=limit,
            include_inactive=True,
            conditions=conditions,
        )

        return build_page(items, total, page, limit)

    # ------------------------------------------------------------------
    # Escritura
    # ------------------------------------------------------------------
    def build_entity(self, data: HorarioCreate) -> Horario:
        ficha_trimestre = self.resolve(
            FichaTrimestreRepository,
            data.ficha_trimestre_uuid,
            "La programación de ficha por trimestre no existe o está inactiva.",
        )

        values = {
            "ficha_trimestre": ficha_trimestre,
            "dia": self._dia(data.dia_uuid),
            "franja": self._franja(data.franja_uuid),
            "resultado": self._resultado(data.resultado_uuid),
            "instructor": self._instructor(data.instructor_uuid),
            "modalidad": data.modalidad,
            "ambiente": self._ambiente(data.ambiente_uuid) if data.ambiente_uuid else None,
        }

        self._validate(values, exclude_id=None)

        return Horario(
            ficha_trimestre=ficha_trimestre,
            trimestre_id=ficha_trimestre.trimestre_id,
            dia=values["dia"],
            franja=values["franja"],
            resultado=values["resultado"],
            instructor=values["instructor"],
            modalidad=values["modalidad"],
            ambiente=values["ambiente"],
            observacion=data.observacion,
        )

    def apply_update(self, entity: Horario, update_data: dict) -> None:
        values = {
            "ficha_trimestre": entity.ficha_trimestre,
            "dia": entity.dia,
            "franja": entity.franja,
            "resultado": entity.resultado,
            "instructor": entity.instructor,
            "modalidad": entity.modalidad,
            "ambiente": entity.ambiente,
        }

        if "dia_uuid" in update_data:
            values["dia"] = self._dia(update_data["dia_uuid"])

        if "franja_uuid" in update_data:
            values["franja"] = self._franja(update_data["franja_uuid"])

        if "resultado_uuid" in update_data:
            values["resultado"] = self._resultado(update_data["resultado_uuid"])

        if "instructor_uuid" in update_data:
            values["instructor"] = self._instructor(update_data["instructor_uuid"])

        if "modalidad" in update_data:
            values["modalidad"] = update_data["modalidad"]

            # Pasar a sincrónico libera el ambiente automáticamente
            if values["modalidad"] == ModalidadClase.SINCRONICO and "ambiente_uuid" not in update_data:
                values["ambiente"] = None

        if "ambiente_uuid" in update_data:
            ambiente_uuid = update_data["ambiente_uuid"]
            values["ambiente"] = self._ambiente(ambiente_uuid) if ambiente_uuid else None

        self._validate(values, exclude_id=entity.id)

        entity.dia = values["dia"]
        entity.franja = values["franja"]
        entity.resultado = values["resultado"]
        entity.instructor = values["instructor"]
        entity.modalidad = values["modalidad"]
        entity.ambiente = values["ambiente"]

        if "observacion" in update_data:
            entity.observacion = update_data["observacion"]

    def delete(self, entity_uuid: UUID) -> None:
        """Eliminación física: libera la casilla."""

        entity = self.get(entity_uuid)

        self.repository.delete(entity)

        self._commit(None, "No fue posible eliminar el horario.")

    def activate(self, entity_uuid: UUID):
        raise ConflictException("Los horarios se eliminan definitivamente; no se reactivan.")

    # ------------------------------------------------------------------
    # Grilla (el horario como el archivo PDF)
    # ------------------------------------------------------------------
    def get_grilla(self, ficha_trimestre_uuid: UUID) -> dict:
        ficha_trimestre = FichaTrimestreRepository(self.db).get_by_uuid(
            ficha_trimestre_uuid,
            include_inactive=False,
        )

        if not ficha_trimestre:
            raise NotFoundException("Programación de ficha por trimestre no encontrada.")

        dias, franjas = self.get_calendario()

        casillas = self.repository.get_by_ficha_trimestre(ficha_trimestre.id)

        horas_programadas = sum(
            self.duracion_horas(h.franja) for h in casillas
        )

        aprendices = self.db.scalar(
            select(func.count())
            .select_from(ficha_aprendiz)
            .where(ficha_aprendiz.c.ficha_id == ficha_trimestre.ficha_id)
        ) or 0

        ficha = ficha_trimestre.ficha
        trimestre = ficha_trimestre.trimestre

        return {
            "encabezado": {
                "ficha_trimestre_uuid": ficha_trimestre.uuid,
                "nombre_grupo": (
                    f"{ficha_trimestre.trimestre_ficha}_TRM_{ficha.codigo}_"
                    f"{ficha.programa.nombre}"
                ),
                "ficha": ficha.codigo,
                "programa": ficha.programa.nombre,
                "trimestre_ficha": ficha_trimestre.trimestre_ficha,
                "anio": trimestre.anio,
                "trimestre_anio": trimestre.numero,
                "fecha_inicio": trimestre.fecha_inicio,
                "fecha_fin": trimestre.fecha_fin,
                "horas_semanales": ficha_trimestre.horas_semanales,
                "horas_programadas": round(horas_programadas, 2),
                "aprendices": aprendices,
            },
            "dias": dias,
            "jornadas": self.build_jornadas(dias, franjas, casillas, self._clase),
        }

    def get_calendario(self) -> tuple[list[DiaSemana], list[FranjaHoraria]]:
        """Columnas (días) y filas (franjas) activas del horario."""

        dias = list(
            self.db.scalars(
                select(DiaSemana)
                .where(DiaSemana.is_active.is_(True))
                .order_by(DiaSemana.numero)
            ).all()
        )

        franjas = list(
            self.db.scalars(
                select(FranjaHoraria)
                .where(FranjaHoraria.is_active.is_(True))
                .order_by(FranjaHoraria.orden)
            ).unique().all()
        )

        return dias, franjas

    @staticmethod
    def build_jornadas(
        dias: list[DiaSemana],
        franjas: list[FranjaHoraria],
        casillas: list[Horario],
        build_clase,
    ) -> list[dict]:
        """Arma la cuadrícula: jornada -> franjas -> una celda por día."""

        por_celda = {(h.franja_id, h.dia_id): h for h in casillas}

        jornadas: dict[str, list] = defaultdict(list)

        for franja in franjas:
            celdas = []

            for dia in dias:
                horario = por_celda.get((franja.id, dia.id))

                celdas.append({
                    "dia_numero": dia.numero,
                    "dia": dia.nombre,
                    "clase": build_clase(horario) if horario else None,
                })

            jornadas[franja.jornada.nombre].append({
                "franja_uuid": franja.uuid,
                "hora_inicio": franja.hora_inicio,
                "hora_fin": franja.hora_fin,
                "celdas": celdas,
            })

        return [
            {"jornada": nombre, "franjas": filas}
            for nombre, filas in jornadas.items()
        ]

    # ------------------------------------------------------------------
    # Validaciones
    # ------------------------------------------------------------------
    def _validate(self, values: dict, exclude_id: int | None) -> None:
        ficha_trimestre: FichaTrimestre = values["ficha_trimestre"]
        modalidad = values["modalidad"]
        ambiente = values["ambiente"]
        dia = values["dia"]
        franja = values["franja"]

        if modalidad == ModalidadClase.PRESENCIAL and ambiente is None:
            raise ValidationException("Una clase presencial requiere ambiente.")

        if modalidad == ModalidadClase.SINCRONICO and ambiente is not None:
            raise ValidationException("Una clase sincrónica no debe tener ambiente.")

        if values["resultado"].competencia.programa_id != ficha_trimestre.ficha.programa_id:
            raise ValidationException(
                "El resultado de aprendizaje no pertenece al programa de la ficha."
            )

        celda = (
            Horario.dia_id == dia.id,
            Horario.franja_id == franja.id,
        )

        cuando = f"{dia.nombre} {self._rango(franja)}"

        choque = self.repository.find_conflict(
            Horario.ficha_trimestre_id == ficha_trimestre.id,
            *celda,
            exclude_id=exclude_id,
        )

        if choque:
            raise ConflictException(f"La ficha ya tiene una clase el {cuando}.")

        choque = self.repository.find_conflict(
            Horario.trimestre_id == ficha_trimestre.trimestre_id,
            Horario.instructor_id == values["instructor"].id,
            *celda,
            exclude_id=exclude_id,
        )

        if choque:
            raise ConflictException(
                f"El instructor ya tiene clase el {cuando} "
                f"con la ficha {choque.ficha_trimestre.ficha.codigo}."
            )

        if ambiente is not None:
            choque = self.repository.find_conflict(
                Horario.trimestre_id == ficha_trimestre.trimestre_id,
                Horario.ambiente_id == ambiente.id,
                *celda,
                exclude_id=exclude_id,
            )

            if choque:
                raise ConflictException(
                    f"El ambiente {ambiente.nombre} ya está ocupado el {cuando} "
                    f"por la ficha {choque.ficha_trimestre.ficha.codigo}."
                )

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def _dia(self, dia_uuid: UUID) -> DiaSemana:
        return self.resolve(DiaSemanaRepository, dia_uuid, "El día indicado no existe o está inactivo.")

    def _franja(self, franja_uuid: UUID) -> FranjaHoraria:
        return self.resolve(
            FranjaHorariaRepository,
            franja_uuid,
            "La franja horaria indicada no existe o está inactiva.",
        )

    def _resultado(self, resultado_uuid: UUID) -> ResultadoAprendizaje:
        return self.resolve(
            ResultadoAprendizajeRepository,
            resultado_uuid,
            "El resultado de aprendizaje indicado no existe o está inactivo.",
        )

    def _ambiente(self, ambiente_uuid: UUID) -> Ambiente:
        return self.resolve(
            AmbienteRepository,
            ambiente_uuid,
            "El ambiente indicado no existe o está inactivo.",
        )

    def _instructor(self, instructor_uuid: UUID) -> User:
        user = UserRepository(self.db).get_by_uuid(
            user_uuid=instructor_uuid,
            include_inactive=False,
        )

        if not user:
            raise ValidationException("El instructor indicado no existe o está inactivo.")

        if user.role != UserRole.INSTRUCTOR:
            raise ValidationException("El usuario indicado no tiene rol instructor.")

        return user

    @staticmethod
    def _rango(franja: FranjaHoraria) -> str:
        return f"{franja.hora_inicio:%H:%M}-{franja.hora_fin:%H:%M}"

    @staticmethod
    def duracion_horas(franja: FranjaHoraria) -> float:
        inicio = franja.hora_inicio.hour * 60 + franja.hora_inicio.minute
        fin = franja.hora_fin.hour * 60 + franja.hora_fin.minute

        return (fin - inicio) / 60

    @staticmethod
    def ambiente_texto(horario: Horario) -> str:
        if horario.modalidad == ModalidadClase.SINCRONICO:
            return "Sincrónico"

        return f"{horario.ambiente.nombre} {horario.ambiente.sede.nombre}"

    @classmethod
    def _clase(cls, horario: Horario) -> dict:
        ambiente = cls.ambiente_texto(horario)

        return {
            "horario_uuid": horario.uuid,
            "tematica": f"{horario.resultado.codigo}. {horario.resultado.descripcion}",
            "resultado_codigo": horario.resultado.codigo,
            "instructor": horario.instructor.name,
            "instructor_uuid": horario.instructor.uuid,
            "modalidad": horario.modalidad,
            "ambiente": ambiente,
        }
