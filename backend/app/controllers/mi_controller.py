from uuid import UUID

from app.models.user import User
from app.services.mi_service import MiService


class MiController:

    def __init__(self, service: MiService):
        self.service = service

    def get_mis_fichas(self, user: User):
        return self.service.get_mis_fichas(user)

    def get_mis_programas(self, user: User):
        return self.service.get_mis_programas(user)

    def get_horario_ficha(
        self,
        user: User,
        ficha_trimestre_uuid: UUID,
    ):
        return self.service.get_horario_ficha(user, ficha_trimestre_uuid)

    def get_mi_agenda(
        self,
        user: User,
        trimestre_uuid: UUID | None,
    ):
        return self.service.get_mi_agenda(user, trimestre_uuid)
