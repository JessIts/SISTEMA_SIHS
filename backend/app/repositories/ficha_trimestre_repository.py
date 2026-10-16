from app.models.ficha_trimestre import FichaTrimestre
from app.repositories.base_repository import BaseRepository


class FichaTrimestreRepository(BaseRepository[FichaTrimestre]):

    model = FichaTrimestre

    def default_order(self) -> list:
        return [FichaTrimestre.id]
