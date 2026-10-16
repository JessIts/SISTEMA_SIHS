from uuid import UUID

from app.models.actividad_aprendizaje import ActividadAprendizaje
from app.models.resultado_aprendizaje import ResultadoAprendizaje
from app.repositories.actividad_aprendizaje_repository import ActividadAprendizajeRepository
from app.repositories.resultado_aprendizaje_repository import ResultadoAprendizajeRepository
from app.schemas.actividad_aprendizaje import ActividadAprendizajeCreate
from app.services.base_service import BaseService


class ActividadAprendizajeService(BaseService[ActividadAprendizaje]):

    repository_class = ActividadAprendizajeRepository
    entity_label = "actividad de aprendizaje"
    female = True

    constraint_messages = {
        "uq_actividades_resultado_codigo": "Ya existe una actividad con ese código en el resultado.",
        "ck_actividades_duracion": "La duración debe ser mayor que cero.",
    }

    def _resultado(self, resultado_uuid: UUID) -> ResultadoAprendizaje:
        return self.resolve(
            ResultadoAprendizajeRepository,
            resultado_uuid,
            "El resultado de aprendizaje indicado no existe o está inactivo.",
        )

    def build_conditions(self, resultado_uuid: UUID | None = None) -> list:
        conditions = []

        if resultado_uuid:
            conditions.append(
                ActividadAprendizaje.resultado.has(ResultadoAprendizaje.uuid == resultado_uuid)
            )

        return conditions

    def build_entity(self, data: ActividadAprendizajeCreate) -> ActividadAprendizaje:
        values = data.model_dump(exclude={"resultado_uuid"})

        return ActividadAprendizaje(**values, resultado=self._resultado(data.resultado_uuid))

    def apply_update(self, entity: ActividadAprendizaje, update_data: dict) -> None:
        if "resultado_uuid" in update_data:
            entity.resultado = self._resultado(update_data.pop("resultado_uuid"))

        super().apply_update(entity, update_data)
