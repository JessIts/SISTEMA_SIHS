from app.models.programa import Programa
from app.repositories.base_repository import BaseRepository


class ProgramaRepository(BaseRepository[Programa]):

    model = Programa

    def default_order(self) -> list:
        return [Programa.codigo]
