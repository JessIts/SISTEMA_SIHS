from unittest.mock import MagicMock

import pytest

from app.core.exceptions import UnauthorizedException
from app.models.roles import UserRole
from app.models.user import User
from app.services.auth_service import AuthService


def test_authenticate_user_success():
    db = MagicMock()
    repository = MagicMock()
    service = AuthService(db)
    service.repository = repository

    user = User(
        name="Angel Gomez",
        email="angel@example.com",
        phone="3001234567",
        document_number="1234567890",
        password_hash="$argon2id$v=19$m=65536,t=3,p=4$dummy",
        role=UserRole.USER,
        is_active=True,
    )

    repository.get_by_email.return_value = user

    # Usamos un hash real para que la prueba no dependa de un hash inventado.
    from app.core.security import hash_password

    user.password_hash = hash_password("Password123!")

    result = service.authenticate_user(
        "angel@example.com",
        "Password123!",
    )

    assert result is user
    repository.get_by_email.assert_called_once_with("angel@example.com")
    
def test_authenticate_user_not_found():
    db = MagicMock()
    repository = MagicMock()
    service = AuthService(db)
    service.repository = repository

    repository.get_by_email.return_value = None

    with pytest.raises(UnauthorizedException) as exc_info:
        service.authenticate_user(
            "missing@example.com",
            "Password123!",
        )

    assert exc_info.value.message == "Credenciales inválidas."
    
def test_authenticate_user_invalid_password():
    db = MagicMock()
    repository = MagicMock()
    service = AuthService(db)
    service.repository = repository

    user = User(
        name="Angel Gomez",
        email="angel@example.com",
        phone="3001234567",
        document_number="1234567890",
        password_hash="",
        role=UserRole.USER,
        is_active=True,
    )

    from app.core.security import hash_password

    user.password_hash = hash_password("CorrectPassword123!")

    repository.get_by_email.return_value = user

    with pytest.raises(UnauthorizedException) as exc_info:
        service.authenticate_user(
            "angel@example.com",
            "WrongPassword123!",
        )

    assert exc_info.value.message == "Credenciales inválidas."
    
def test_authenticate_user_inactive():
    db = MagicMock()
    repository = MagicMock()
    service = AuthService(db)
    service.repository = repository

    from app.core.security import hash_password

    user = User(
        name="Angel Gomez",
        email="angel@example.com",
        phone="3001234567",
        document_number="1234567890",
        password_hash=hash_password("Password123!"),
        role=UserRole.USER,
        is_active=False,
    )

    repository.get_by_email.return_value = user

    with pytest.raises(UnauthorizedException) as exc_info:
        service.authenticate_user(
            "angel@example.com",
            "Password123!",
        )

    assert exc_info.value.message == "Usuario inactivo."