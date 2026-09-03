from app.models.user import User
from app.schemas.register import RegisterRequest
from app.services.register_service import RegisterService


class RegisterController:

    def __init__(self, service: RegisterService):
        self.service = service

    def register(
        self,
        data: RegisterRequest,
    ) -> User:

        return self.service.register(data)