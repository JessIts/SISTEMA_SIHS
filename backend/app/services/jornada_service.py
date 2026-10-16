from app.models.jornada import Jornada
from app.repositories.jornada_repository import JornadaRepository
from app.schemas.jornada import JornadaCreate
from app.services.base_service import BaseService


class JornadaService(BaseService[Jornada]):

    repository_class = JornadaRepository
    entity_label = "jornada"
    female = True

    constraint_messages = {
        "jornadas_nombre_key": "Ya existe una jornada con ese nombre.",
    }

    dependents = [
        ("franjas", "No se puede desactivar la jornada: tiene franjas horarias activas."),
        ("fichas", "No se puede desactivar la jornada: tiene fichas activas."),
    ]

    def build_entity(self, data: JornadaCreate) -> Jornada:
        return Jornada(nombre=data.nombre.upper())

    def apply_update(self, entity: Jornada, update_data: dict) -> None:
        if update_data.get("nombre"):
            update_data["nombre"] = update_data["nombre"].upper()

        super().apply_update(entity, update_data)
