from uuid import UUID

from app.controllers.base_controller import BaseController
from app.services.ficha_service import FichaService


class FichaController(BaseController[FichaService]):

    def get_aprendices(self, ficha_uuid: UUID):
        return self.service.get_aprendices(ficha_uuid)

    def add_aprendiz(
        self,
        ficha_uuid: UUID,
        user_uuid: UUID,
    ):
        return self.service.add_aprendiz(ficha_uuid, user_uuid)

    def remove_aprendiz(
        self,
        ficha_uuid: UUID,
        user_uuid: UUID,
    ):
        self.service.remove_aprendiz(ficha_uuid, user_uuid)
