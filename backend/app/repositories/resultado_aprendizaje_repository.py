from app.models.resultado_aprendizaje import ResultadoAprendizaje
from app.repositories.base_repository import BaseRepository


class ResultadoAprendizajeRepository(BaseRepository[ResultadoAprendizaje]):

    model = ResultadoAprendizaje

    def default_order(self) -> list:
        return [ResultadoAprendizaje.competencia_id, ResultadoAprendizaje.codigo]
