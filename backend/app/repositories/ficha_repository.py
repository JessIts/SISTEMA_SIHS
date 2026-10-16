from app.models.ficha import Ficha
from app.repositories.base_repository import BaseRepository


class FichaRepository(BaseRepository[Ficha]):

    model = Ficha

    def default_order(self) -> list:
        return [Ficha.codigo]
