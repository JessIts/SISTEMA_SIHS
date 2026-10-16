from app.models.sede import Sede
from app.repositories.sede_repository import SedeRepository
from app.schemas.sede import SedeCreate
from app.services.base_service import BaseService


class SedeService(BaseService[Sede]):

    repository_class = SedeRepository
    entity_label = "sede"
    female = True

    constraint_messages = {
        "sedes_nombre_key": "Ya existe una sede con ese nombre.",
    }

    dependents = [
        ("ambientes", "No se puede desactivar la sede: tiene ambientes activos."),
    ]

    def build_entity(self, data: SedeCreate) -> Sede:
        return Sede(**data.model_dump())
