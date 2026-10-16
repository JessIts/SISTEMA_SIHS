from uuid import UUID

from app.models.competencia import Competencia
from app.models.programa import Programa
from app.models.resultado_aprendizaje import ResultadoAprendizaje
from app.repositories.competencia_repository import CompetenciaRepository
from app.repositories.resultado_aprendizaje_repository import ResultadoAprendizajeRepository
from app.schemas.resultado_aprendizaje import ResultadoAprendizajeCreate
from app.services.base_service import BaseService


class ResultadoAprendizajeService(BaseService[ResultadoAprendizaje]):

    repository_class = ResultadoAprendizajeRepository
    entity_label = "resultado de aprendizaje"

    constraint_messages = {
        "uq_resultados_competencia_codigo": "Ya existe un resultado con ese código en la competencia.",
    }

    dependents = [
        ("actividades", "No se puede desactivar el resultado: tiene actividades activas."),
    ]

    def _competencia(self, competencia_uuid: UUID) -> Competencia:
        return self.resolve(
            CompetenciaRepository,
            competencia_uuid,
            "La competencia indicada no existe o está inactiva.",
        )

    def build_conditions(
        self,
        competencia_uuid: UUID | None = None,
        programa_uuid: UUID | None = None,
    ) -> list:
        conditions = []

        if programa_uuid:
            conditions.append(
                ResultadoAprendizaje.competencia.has(
                    Competencia.programa.has(Programa.uuid == programa_uuid)
                )
            )

        if competencia_uuid:
            conditions.append(
                ResultadoAprendizaje.competencia.has(Competencia.uuid == competencia_uuid)
            )

        return conditions

    def build_entity(self, data: ResultadoAprendizajeCreate) -> ResultadoAprendizaje:
        values = data.model_dump(exclude={"competencia_uuid"})

        return ResultadoAprendizaje(
            **values,
            competencia=self._competencia(data.competencia_uuid),
        )

    def apply_update(self, entity: ResultadoAprendizaje, update_data: dict) -> None:
        if "competencia_uuid" in update_data:
            entity.competencia = self._competencia(update_data.pop("competencia_uuid"))

        super().apply_update(entity, update_data)
