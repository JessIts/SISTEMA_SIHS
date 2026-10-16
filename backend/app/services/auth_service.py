from sqlalchemy.orm import Session

from app.core.exceptions import UnauthorizedException
from app.core.security import create_access_token, verify_password
from app.repositories.user_repository import UserRepository


class AuthService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def authenticate_user(self, email: str, password: str):
        user = self.repository.get_by_email(email)

        if not user:
            raise UnauthorizedException(
                "Credenciales inválidas."
            )

        if not verify_password(
            password,
            user.password_hash,
        ):
            raise UnauthorizedException(
                "Credenciales inválidas."
            )

        if not user.is_active:
            raise UnauthorizedException(
                "Usuario inactivo."
            )

        access_token = create_access_token(
            str(user.uuid)
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }