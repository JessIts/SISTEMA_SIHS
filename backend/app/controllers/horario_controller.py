from uuid import UUID

from app.controllers.base_controller import BaseController
from app.services.horario_service import HorarioService


class HorarioController(BaseController[HorarioService]):

    def get_grilla(self, ficha_trimestre_uuid: UUID):
        return self.service.get_grilla(ficha_trimestre_uuid)
