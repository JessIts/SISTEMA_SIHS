from uuid import UUID

from app.controllers.base_controller import BaseController
from app.services.coordinacion_service import CoordinacionService


class CoordinacionController(BaseController[CoordinacionService]):

    def add_sede(
        self,
        coordinacion_uuid: UUID,
        sede_uuid: UUID,
    ):
        return self.service.add_sede(coordinacion_uuid, sede_uuid)

    def remove_sede(
        self,
        coordinacion_uuid: UUID,
        sede_uuid: UUID,
    ):
        return self.service.remove_sede(coordinacion_uuid, sede_uuid)
