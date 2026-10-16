from uuid import UUID

from app.models.ambiente import Ambiente
from app.models.sede import Sede
from app.repositories.ambiente_repository import AmbienteRepository
from app.repositories.sede_repository import SedeRepository
from app.schemas.ambiente import AmbienteCreate
from app.services.base_service import BaseService


class AmbienteService(BaseService[Ambiente]):

    repository_class = AmbienteRepository
    entity_label = "ambiente"

    constraint_messages = {
        "uq_ambientes_sede_nombre": "Ya existe un ambiente con ese nombre en la sede.",
        "ck_ambientes_capacidad": "La capacidad debe ser mayor que cero.",
    }

    def _sede(self, sede_uuid: UUID) -> Sede:
        return self.resolve(
            SedeRepository,
            sede_uuid,
            "La sede indicada no existe o está inactiva.",
        )

    def build_conditions(self, sede_uuid: UUID | None = None) -> list:
        conditions = []

        if sede_uuid:
            conditions.append(Ambiente.sede.has(Sede.uuid == sede_uuid))

        return conditions

    def build_entity(self, data: AmbienteCreate) -> Ambiente:
        values = data.model_dump(exclude={"sede_uuid"})

        return Ambiente(**values, sede=self._sede(data.sede_uuid))

    def apply_update(self, entity: Ambiente, update_data: dict) -> None:
        if "sede_uuid" in update_data:
            entity.sede = self._sede(update_data.pop("sede_uuid"))

        super().apply_update(entity, update_data)
