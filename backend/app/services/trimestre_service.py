from app.models.trimestre import Trimestre
from app.repositories.trimestre_repository import TrimestreRepository
from app.schemas.trimestre import TrimestreCreate
from app.services.base_service import BaseService


class TrimestreService(BaseService[Trimestre]):

    repository_class = TrimestreRepository
    entity_label = "trimestre"

    constraint_messages = {
        "uq_trimestres_anio_numero": "Ya existe ese trimestre para el año indicado.",
        "ck_trimestres_fechas": "La fecha de fin debe ser posterior a la fecha de inicio.",
        "ck_trimestres_numero": "El número del trimestre debe estar entre 1 y 4.",
    }

    dependents = [
        ("fichas_trimestre", "No se puede desactivar el trimestre: tiene fichas programadas."),
    ]

    def build_entity(self, data: TrimestreCreate) -> Trimestre:
        return Trimestre(**data.model_dump())
