from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.ambiente import Ambiente
from app.models.enums import EstadoTrimestre
from app.models.ficha import Ficha
from app.models.ficha_trimestre import FichaTrimestre
from app.models.horario import Horario
from app.models.programa import Programa
from app.models.sede import Sede
from app.models.trimestre import Trimestre
from app.models.user import User
from app.services.horario_service import HorarioService


class DashboardService:
    """Resumen para los tableros de administración y coordinación."""

    def __init__(self, db: Session):
        self.db = db

    def _contar_activos(self, model) -> int:
        return self.db.scalar(
            select(func.count()).select_from(model).where(model.is_active.is_(True))
        ) or 0

    def get_resumen(self) -> dict:
        usuarios = dict(
            self.db.execute(
                select(User.role, func.count())
                .where(User.is_active.is_(True))
                .group_by(User.role)
            ).all()
        )

        trimestres_vigentes = list(
            self.db.scalars(
                select(Trimestre)
                .where(
                    Trimestre.is_active.is_(True),
                    Trimestre.estado.in_([EstadoTrimestre.ACTIVO, EstadoTrimestre.PLANEACION]),
                )
                .order_by(Trimestre.anio.desc(), Trimestre.numero.desc())
            ).all()
        )

        programaciones = []

        if trimestres_vigentes:
            fichas_trimestre = self.db.scalars(
                select(FichaTrimestre)
                .where(
                    FichaTrimestre.is_active.is_(True),
                    FichaTrimestre.trimestre_id.in_([t.id for t in trimestres_vigentes]),
                )
            ).unique().all()

            for ft in fichas_trimestre:
                horas = sum(
                    HorarioService.duracion_horas(h.franja) for h in ft.horarios
                )

                programaciones.append({
                    "ficha_trimestre_uuid": ft.uuid,
                    "ficha": ft.ficha.codigo,
                    "programa": ft.ficha.programa.nombre,
                    "trimestre_ficha": ft.trimestre_ficha,
                    "trimestre": f"{ft.trimestre.anio}-T{ft.trimestre.numero}",
                    "horas_semanales": ft.horas_semanales,
                    "horas_programadas": round(horas, 2),
                })

            # Primero las que tienen menos horas programadas (las que faltan por armar)
            programaciones.sort(
                key=lambda p: (p["horas_programadas"] / p["horas_semanales"], p["ficha"])
            )

        return {
            "conteos": {
                "sedes": self._contar_activos(Sede),
                "ambientes": self._contar_activos(Ambiente),
                "programas": self._contar_activos(Programa),
                "fichas": self._contar_activos(Ficha),
                "trimestres": self._contar_activos(Trimestre),
                "horarios": self.db.scalar(select(func.count()).select_from(Horario)) or 0,
            },
            "usuarios": {role.value: total for role, total in usuarios.items()},
            "trimestres_activos": [
                t for t in trimestres_vigentes if t.estado == EstadoTrimestre.ACTIVO
            ],
            "programaciones": programaciones,
        }
