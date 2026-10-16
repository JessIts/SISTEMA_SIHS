from app.models.actividad_aprendizaje import ActividadAprendizaje
from app.repositories.base_repository import BaseRepository


class ActividadAprendizajeRepository(BaseRepository[ActividadAprendizaje]):

    model = ActividadAprendizaje

    def default_order(self) -> list:
        return [ActividadAprendizaje.resultado_id, ActividadAprendizaje.codigo]
