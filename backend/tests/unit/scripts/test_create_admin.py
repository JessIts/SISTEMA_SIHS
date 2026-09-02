from unittest.mock import MagicMock
import pytest
from unittest.mock import patch

from app.models.roles import UserRole
from scripts.create_admin import create_admin


def test_create_admin_promotes_existing_user():
    # Arrange
    db = MagicMock()

    user_uuid = "550e8400-e29b-41d4-a716-446655440000"

    user = MagicMock()
    user.uuid = user_uuid
    user.email = "angel@example.com"
    user.role = UserRole.USER

    repository = MagicMock()
    repository.get_by_email.return_value = user

    service = MagicMock()
    service.repository = repository
    service.promote_to_admin.return_value = user

    # Act
    result = create_admin(
        email="angel@example.com",
        db=db,
        service=service,
    )

    # Assert
    assert result == user

    service.repository.get_by_email.assert_called_once_with(
        "angel@example.com",
    )
    service.promote_to_admin.assert_called_once_with(user_uuid)
    
def test_create_admin_returns_none_when_user_not_found():
    # Arrange
    db = MagicMock()

    repository = MagicMock()
    repository.get_by_email.return_value = None

    service = MagicMock()
    service.repository = repository

    # Act
    result = create_admin(
        email="missing@example.com",
        db=db,
        service=service,
    )

    # Assert
    assert result is None

    service.repository.get_by_email.assert_called_once_with(
        "missing@example.com",
    )
    service.promote_to_admin.assert_not_called()
    
def test_create_admin_propagates_promotion_error():
    # Arrange
    db = MagicMock()

    user_uuid = "550e8400-e29b-41d4-a716-446655440000"

    user = MagicMock()
    user.uuid = user_uuid
    user.email = "angel@example.com"

    repository = MagicMock()
    repository.get_by_email.return_value = user

    service = MagicMock()
    service.repository = repository

    error = RuntimeError("Error al promover usuario.")
    service.promote_to_admin.side_effect = error

    # Act / Assert
    with pytest.raises(RuntimeError, match="Error al promover usuario."):
        create_admin(
            email="angel@example.com",
            db=db,
            service=service,
        )

    service.repository.get_by_email.assert_called_once_with(
        "angel@example.com",
    )
    service.promote_to_admin.assert_called_once_with(user_uuid)
    
def test_main_creates_database_session_and_promotes_user():
    # Arrange
    user = MagicMock()

    db = MagicMock()

    service = MagicMock()
    service.repository.get_by_email.return_value = user
    service.promote_to_admin.return_value = user

    # Act
    with patch("scripts.create_admin.SessionLocal", return_value=db), \
         patch("scripts.create_admin.UserService", return_value=service), \
         patch("sys.argv", ["create_admin", "angel@example.com"]):

        from scripts.create_admin import main

        result = main()

    # Assert
    assert result == user

    service.repository.get_by_email.assert_called_once_with(
        "angel@example.com",
    )
    service.promote_to_admin.assert_called_once_with(user.uuid)

    db.close.assert_called_once()
    
def test_main_requires_email():
    # Arrange
    with patch("sys.argv", ["create_admin"]):
        from scripts.create_admin import main

        # Act / Assert
        with pytest.raises(SystemExit):
            main()