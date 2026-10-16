from uuid import UUID

from app.models.coordinacion import Coordinacion
from app.models.programa import Programa
from app.repositories.coordinacion_repository import CoordinacionRepository
from app.repositories.programa_repository import ProgramaRepository
from app.schemas.programa import ProgramaCreate
from app.services.base_service import BaseService


class ProgramaService(BaseService[Programa]):

    repository_class = ProgramaRepository
    entity_label = "programa"

    constraint_messages = {
        "programas_codigo_key": "Ya existe un programa con ese código.",
    }

    dependents = [
        ("competencias", "No se puede desactivar el programa: tiene competencias activas."),
        ("fichas", "No se puede desactivar el programa: tiene fichas activas."),
    ]

    def _coordinacion(self, coordinacion_uuid: UUID) -> Coordinacion:
        return self.resolve(
            CoordinacionRepository,
            coordinacion_uuid,
            "La coordinación indicada no existe o está inactiva.",
        )

    def build_conditions(self, coordinacion_uuid: UUID | None = None) -> list:
        conditions = []

        if coordinacion_uuid:
            conditions.append(
                Programa.coordinacion.has(Coordinacion.uuid == coordinacion_uuid)
            )

        return conditions

    def build_entity(self, data: ProgramaCreate) -> Programa:
        values = data.model_dump(exclude={"coordinacion_uuid"})

        return Programa(
            **values,
            coordinacion=self._coordinacion(data.coordinacion_uuid),
        )

    def apply_update(self, entity: Programa, update_data: dict) -> None:
        if "coordinacion_uuid" in update_data:
            entity.coordinacion = self._coordinacion(
                update_data.pop("coordinacion_uuid")
            )

        super().apply_update(entity, update_data)
