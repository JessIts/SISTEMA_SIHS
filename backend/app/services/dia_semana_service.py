from app.models.dia_semana import DiaSemana
from app.repositories.dia_semana_repository import DiaSemanaRepository
from app.schemas.dia_semana import DiaSemanaCreate
from app.services.base_service import BaseService


class DiaSemanaService(BaseService[DiaSemana]):

    repository_class = DiaSemanaRepository
    entity_label = "día"

    constraint_messages = {
        "dias_semana_numero_key": "Ya existe un día con ese número.",
        "dias_semana_nombre_key": "Ya existe un día con ese nombre.",
        "ck_dias_semana_numero": "El número del día debe estar entre 1 y 7.",
    }

    def build_entity(self, data: DiaSemanaCreate) -> DiaSemana:
        return DiaSemana(numero=data.numero, nombre=data.nombre.upper())

    def apply_update(self, entity: DiaSemana, update_data: dict) -> None:
        if update_data.get("nombre"):
            update_data["nombre"] = update_data["nombre"].upper()

        super().apply_update(entity, update_data)
