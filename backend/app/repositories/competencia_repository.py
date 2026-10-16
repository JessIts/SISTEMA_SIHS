from app.models.competencia import Competencia
from app.repositories.base_repository import BaseRepository


class CompetenciaRepository(BaseRepository[Competencia]):

    model = Competencia

    def default_order(self) -> list:
        return [Competencia.programa_id, Competencia.codigo]
