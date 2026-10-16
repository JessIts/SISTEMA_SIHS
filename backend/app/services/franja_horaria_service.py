from uuid import UUID

from app.models.franja_horaria import FranjaHoraria
from app.models.jornada import Jornada
from app.repositories.franja_horaria_repository import FranjaHorariaRepository
from app.repositories.jornada_repository import JornadaRepository
from app.schemas.franja_horaria import FranjaHorariaCreate
from app.services.base_service import BaseService


class FranjaHorariaService(BaseService[FranjaHoraria]):

    repository_class = FranjaHorariaRepository
    entity_label = "franja horaria"
    female = True

    constraint_messages = {
        "uq_franjas_horas": "Ya existe una franja con esa hora de inicio y fin.",
        "franjas_horarias_orden_key": "Ya existe una franja con ese orden.",
        "ck_franjas_horas": "La hora de fin debe ser mayor que la hora de inicio.",
    }

    def _jornada(self, jornada_uuid: UUID) -> Jornada:
        return self.resolve(
            JornadaRepository,
            jornada_uuid,
            "La jornada indicada no existe o está inactiva.",
        )

    def build_conditions(self, jornada_uuid: UUID | None = None) -> list:
        conditions = []

        if jornada_uuid:
            conditions.append(FranjaHoraria.jornada.has(Jornada.uuid == jornada_uuid))

        return conditions

    def build_entity(self, data: FranjaHorariaCreate) -> FranjaHoraria:
        values = data.model_dump(exclude={"jornada_uuid"})

        return FranjaHoraria(**values, jornada=self._jornada(data.jornada_uuid))

    def apply_update(self, entity: FranjaHoraria, update_data: dict) -> None:
        if "jornada_uuid" in update_data:
            entity.jornada = self._jornada(update_data.pop("jornada_uuid"))

        super().apply_update(entity, update_data)
