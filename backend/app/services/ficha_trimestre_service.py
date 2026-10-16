from uuid import UUID

from app.core.exceptions import ConflictException
from app.models.ficha import Ficha
from app.models.ficha_trimestre import FichaTrimestre
from app.models.trimestre import Trimestre
from app.repositories.ficha_repository import FichaRepository
from app.repositories.ficha_trimestre_repository import FichaTrimestreRepository
from app.repositories.trimestre_repository import TrimestreRepository
from app.schemas.ficha_trimestre import FichaTrimestreCreate
from app.services.base_service import BaseService


class FichaTrimestreService(BaseService[FichaTrimestre]):

    repository_class = FichaTrimestreRepository
    entity_label = "programación de ficha por trimestre"
    female = True

    constraint_messages = {
        "uq_fichas_trimestre_ficha_trimestre": "La ficha ya está programada en ese trimestre.",
        "uq_fichas_trimestre_ficha_numero": "La ficha ya tiene registrado ese número de trimestre de formación.",
        "ck_fichas_trimestre_horas": "Las horas semanales deben ser mayores que cero.",
        "ck_fichas_trimestre_numero": "El trimestre de formación debe ser mayor que cero.",
    }

    def build_conditions(
        self,
        ficha_uuid: UUID | None = None,
        trimestre_uuid: UUID | None = None,
    ) -> list:
        conditions = []

        if ficha_uuid:
            conditions.append(FichaTrimestre.ficha.has(Ficha.uuid == ficha_uuid))

        if trimestre_uuid:
            conditions.append(FichaTrimestre.trimestre.has(Trimestre.uuid == trimestre_uuid))

        return conditions

    def build_entity(self, data: FichaTrimestreCreate) -> FichaTrimestre:
        ficha = self.resolve(
            FichaRepository,
            data.ficha_uuid,
            "La ficha indicada no existe o está inactiva.",
        )

        trimestre = self.resolve(
            TrimestreRepository,
            data.trimestre_uuid,
            "El trimestre indicado no existe o está inactivo.",
        )

        return FichaTrimestre(
            ficha=ficha,
            trimestre=trimestre,
            trimestre_ficha=data.trimestre_ficha,
            horas_semanales=data.horas_semanales,
        )

    def validate_can_deactivate(self, entity: FichaTrimestre) -> None:
        # Las casillas (horarios) no tienen is_active: basta con que exista una.
        if entity.horarios:
            raise ConflictException(
                "No se puede desactivar: la ficha ya tiene casillas de horario en este trimestre."
            )
