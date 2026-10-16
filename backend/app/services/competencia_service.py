from uuid import UUID

from app.models.competencia import Competencia
from app.models.programa import Programa
from app.repositories.competencia_repository import CompetenciaRepository
from app.repositories.programa_repository import ProgramaRepository
from app.schemas.competencia import CompetenciaCreate
from app.services.base_service import BaseService


class CompetenciaService(BaseService[Competencia]):

    repository_class = CompetenciaRepository
    entity_label = "competencia"
    female = True

    constraint_messages = {
        "uq_competencias_programa_codigo": "Ya existe una competencia con ese código en el programa.",
    }

    dependents = [
        ("resultados", "No se puede desactivar la competencia: tiene resultados de aprendizaje activos."),
    ]

    def _programa(self, programa_uuid: UUID) -> Programa:
        return self.resolve(
            ProgramaRepository,
            programa_uuid,
            "El programa indicado no existe o está inactivo.",
        )

    def build_conditions(self, programa_uuid: UUID | None = None) -> list:
        conditions = []

        if programa_uuid:
            conditions.append(Competencia.programa.has(Programa.uuid == programa_uuid))

        return conditions

    def build_entity(self, data: CompetenciaCreate) -> Competencia:
        values = data.model_dump(exclude={"programa_uuid"})

        return Competencia(**values, programa=self._programa(data.programa_uuid))

    def apply_update(self, entity: Competencia, update_data: dict) -> None:
        if "programa_uuid" in update_data:
            entity.programa = self._programa(update_data.pop("programa_uuid"))

        super().apply_update(entity, update_data)
