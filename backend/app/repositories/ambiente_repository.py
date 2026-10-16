from app.models.ambiente import Ambiente
from app.repositories.base_repository import BaseRepository


class AmbienteRepository(BaseRepository[Ambiente]):

    model = Ambiente

    def default_order(self) -> list:
        return [Ambiente.sede_id, Ambiente.nombre]
