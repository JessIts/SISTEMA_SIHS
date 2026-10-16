from app.models.sede import Sede
from app.repositories.base_repository import BaseRepository


class SedeRepository(BaseRepository[Sede]):

    model = Sede

    def default_order(self) -> list:
        return [Sede.nombre]
