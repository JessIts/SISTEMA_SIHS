from uuid import UUID

from app.schemas.user import UserCreate, UserUpdate
from app.services.user_service import UserService


class UserController:

    def __init__(
        self,
        service: UserService,
    ):
        self.service = service

    def create(
        self,
        data: UserCreate,
    ):
        return self.service.create_user(data)

    def get_all(self):
        return self.service.get_users()

    def get_inactive(self):
        return self.service.get_inactive_users()

    def get_by_uuid(
        self,
        user_uuid: UUID,
    ):
        return self.service.get_user(user_uuid)

    def update(
        self,
        user_uuid: UUID,
        data: UserUpdate,
    ):
        return self.service.update_user(
            user_uuid,
            data,
        )

    def delete(
        self,
        user_uuid: UUID,
    ):
        self.service.delete_user(user_uuid)

    def activate(
        self,
        user_uuid: UUID,
    ):
        return self.service.activate_user(user_uuid)
