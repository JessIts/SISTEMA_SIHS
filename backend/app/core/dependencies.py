from uuid import UUID

import jwt

from fastapi import Depends
from fastapi.security import (
    HTTPAuthorizationCredentials,
    HTTPBearer,
)
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.exceptions import (
    ForbiddenException,
    UnauthorizedException,
)
from app.core.security import decode_access_token
from app.models.roles import UserRole
from app.repositories.user_repository import UserRepository


security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
):
    token = credentials.credentials

    try:
        payload = decode_access_token(token)
        user_uuid = UUID(payload["sub"])

    except (jwt.InvalidTokenError, KeyError, ValueError):
        raise UnauthorizedException("Token inválido.")

    repository = UserRepository(db)

    user = repository.get_by_uuid(
        user_uuid=user_uuid,
        include_inactive=False,
    )

    if not user:
        raise UnauthorizedException(
            "Usuario no encontrado o inactivo."
        )

    return user


def get_current_admin(
    user=Depends(get_current_user),
):
    if user.role != UserRole.ADMIN:
        raise ForbiddenException(
            "Permisos insuficientes."
        )

    return user