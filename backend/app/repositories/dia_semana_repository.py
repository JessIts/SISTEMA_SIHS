from app.models.dia_semana import DiaSemana
from app.repositories.base_repository import BaseRepository


class DiaSemanaRepository(BaseRepository[DiaSemana]):

    model = DiaSemana

    def default_order(self) -> list:
        return [DiaSemana.numero]
