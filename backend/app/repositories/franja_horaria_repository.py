from app.models.franja_horaria import FranjaHoraria
from app.repositories.base_repository import BaseRepository


class FranjaHorariaRepository(BaseRepository[FranjaHoraria]):

    model = FranjaHoraria

    def default_order(self) -> list:
        return [FranjaHoraria.orden]
