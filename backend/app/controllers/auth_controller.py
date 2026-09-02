from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService


class AuthController:
    def __init__(self, service: AuthService):
        self.service = service

    def login(self, data: LoginRequest) -> TokenResponse:
        token = self.service.authenticate_user(
            email=data.email,
            password=data.password,
        )

        return TokenResponse(**token)