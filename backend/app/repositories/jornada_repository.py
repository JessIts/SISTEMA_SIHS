from app.models.jornada import Jornada
from app.repositories.base_repository import BaseRepository


class JornadaRepository(BaseRepository[Jornada]):

    model = Jornada

    def default_order(self) -> list:
        return [Jornada.id]
