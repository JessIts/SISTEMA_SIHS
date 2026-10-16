from app.models.coordinacion import Coordinacion
from app.repositories.base_repository import BaseRepository


class CoordinacionRepository(BaseRepository[Coordinacion]):

    model = Coordinacion

    def default_order(self) -> list:
        return [Coordinacion.nombre]
