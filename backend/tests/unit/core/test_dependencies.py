from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.core.dependencies import get_current_user
from app.core.exceptions import UnauthorizedException, ForbiddenException
from app.core.security import create_access_token
from app.models.roles import UserRole
from app.models.user import User
from fastapi.security import HTTPAuthorizationCredentials
from app.core.dependencies import get_current_admin

def test_get_current_user_success():
    db = MagicMock()
    repository = MagicMock()

    user_uuid = uuid4()

    user = User(
        uuid=user_uuid,
        name="Angel Gomez",
        email="angel@example.com",
        phone="3001234567",
        document_number="1234567890",
        password_hash="hash",
        role=UserRole.USER,
        is_active=True,
    )

    repository.get_by_uuid.return_value = user

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=create_access_token(str(user_uuid)),
    )

    # La función crea internamente UserRepository(db),
    # así que aquí necesitamos parchearlo.
    from unittest.mock import patch

    with patch(
        "app.core.dependencies.UserRepository",
        return_value=repository,
    ):
        result = get_current_user(
            credentials=credentials,
            db=db,
        )

    assert result is user

    repository.get_by_uuid.assert_called_once_with(
        user_uuid=user_uuid,
        include_inactive=False,
    )
    
def test_get_current_user_invalid_token():
    db = MagicMock()

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials="token-invalido",
    )

    with pytest.raises(UnauthorizedException) as exc_info:
        get_current_user(
            credentials=credentials,
            db=db,
        )

    assert exc_info.value.message == "Token inválido."
    
from unittest.mock import patch


def test_get_current_user_invalid_subject():
    db = MagicMock()

    with patch(
        "app.core.dependencies.decode_access_token",
        return_value={"sub": "no-es-un-uuid"},
    ):
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="token-valido",
        )

        with pytest.raises(UnauthorizedException) as exc_info:
            get_current_user(
                credentials=credentials,
                db=db,
            )

    assert exc_info.value.message == "Token inválido."
    
def test_get_current_user_user_not_found():
    db = MagicMock()
    repository = MagicMock()

    user_uuid = uuid4()

    repository.get_by_uuid.return_value = None

    credentials = HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=create_access_token(str(user_uuid)),
    )

    with patch(
        "app.core.dependencies.UserRepository",
        return_value=repository,
    ):
        with pytest.raises(UnauthorizedException) as exc_info:
            get_current_user(
                credentials=credentials,
                db=db,
            )

    assert exc_info.value.message == "Usuario no encontrado o inactivo."
    
def test_get_current_user_missing_subject():
    db = MagicMock()

    with patch(
        "app.core.dependencies.decode_access_token",
        return_value={},
    ):
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="token-valido",
        )

        with pytest.raises(UnauthorizedException) as exc_info:
            get_current_user(
                credentials=credentials,
                db=db,
            )

    assert exc_info.value.message == "Token inválido."
    
def test_get_current_admin_success():
    user = User(
        uuid=uuid4(),
        name="Admin Test",
        email="admin@example.com",
        phone="3001234567",
        document_number="ADMIN-001",
        password_hash="hash",
        role=UserRole.ADMIN,
        is_active=True,
    )

    result = get_current_admin(user=user) 
    
    assert result is user


def test_get_current_admin_forbidden_for_user():
    user = User(
        uuid=uuid4(),
        name="User Test",
        email="user@example.com",
        phone="3001234567",
        document_number="USER-001",
        password_hash="hash",
        role=UserRole.USER,
        is_active=True,
    )

    with pytest.raises(ForbiddenException) as exc_info: get_current_admin(user=user) 

    assert exc_info.value.message == "Permisos insuficientes."