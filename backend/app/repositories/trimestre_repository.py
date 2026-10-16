from app.models.trimestre import Trimestre
from app.repositories.base_repository import BaseRepository


class TrimestreRepository(BaseRepository[Trimestre]):

    model = Trimestre

    def default_order(self) -> list:
        return [Trimestre.anio.desc(), Trimestre.numero.desc()]
