import pytest
from unittest.mock import MagicMock

from app.core.exceptions import ConflictException
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user_service import UserService

from uuid import uuid4
from app.core.exceptions import NotFoundException

def test_create_user_success():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    data = UserCreate(
        name="Angel Gomez",
        email="angel@example.com",
        phone="3001234567",
        document_number="1234567890",
    )

    repository.get_by_email.return_value = None
    repository.get_by_document_number.return_value = None
    repository.create.side_effect = lambda user: user

    # Act
    user = service.create_user(data)

    # Assert
    assert user is not None
    assert user.name == "Angel Gomez"
    assert user.email == "angel@example.com"
    assert user.phone == "3001234567"
    assert user.document_number == "1234567890"

    repository.create.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)


def test_create_user_email_already_exists():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    data = UserCreate(
        name="Angel Gomez",
        email="angel@example.com",
        phone="3001234567",
        document_number="1234567890",
    )

    repository.get_by_email.return_value = MagicMock()

    # Act / Assert
    with pytest.raises(ConflictException) as exc_info:
        service.create_user(data)

    assert str(exc_info.value) == (
        "El correo electrónico ya está registrado."
    )

    repository.create.assert_not_called()
    db.commit.assert_not_called()


def test_create_user_document_already_exists():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    data = UserCreate(
        name="Angel Gomez",
        email="angel@example.com",
        phone="3001234567",
        document_number="1234567890",
    )

    repository.get_by_email.return_value = None
    repository.get_by_document_number.return_value = MagicMock()

    # Act / Assert
    with pytest.raises(ConflictException) as exc_info:
        service.create_user(data)

    assert str(exc_info.value) == (
        "El documento de identidad ya está registrado."
    )

    repository.create.assert_not_called()
    db.commit.assert_not_called()
    

def test_get_user_success():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    expected_user = MagicMock()
    expected_user.uuid = user_uuid
    expected_user.name = "Angel Gomez"

    repository.get_by_uuid.return_value = expected_user

    # Act
    user = service.get_user(user_uuid)

    # Assert
    assert user == expected_user

    repository.get_by_uuid.assert_called_once_with(
        user_uuid=user_uuid,
        include_inactive=False,
    )


def test_get_user_not_found():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    repository.get_by_uuid.return_value = None

    # Act / Assert
    with pytest.raises(NotFoundException) as exc_info:
        service.get_user(user_uuid)

    assert str(exc_info.value) == (
        "Usuario no encontrado."
    )


def test_update_user_success():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    user = MagicMock()
    user.uuid = user_uuid
    user.name = "Angel Gomez"
    user.email = "old@example.com"
    user.phone = "3001234567"

    repository.get_by_uuid.return_value = user
    repository.get_by_email.return_value = None
    repository.update.return_value = user

    data = UserUpdate(
        name="Angel Gomez Updated",
        phone="3109876543",
    )

    # Act
    result = service.update_user(
        user_uuid,
        data,
    )

    # Assert
    assert result == user
    assert user.name == "Angel Gomez Updated"
    assert user.phone == "3109876543"

    repository.update.assert_called_once_with(user)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)


def test_update_user_email_already_exists():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    user = MagicMock()
    user.uuid = user_uuid

    existing_user = MagicMock()
    existing_user.uuid = uuid4()

    repository.get_by_uuid.return_value = user
    repository.get_by_email.return_value = existing_user

    data = UserUpdate(
        email="existing@example.com",
    )
    
    print("user_uuid:", user_uuid)
    print("existing_user.uuid:", existing_user.uuid)
    print(
        "son diferentes:",
        existing_user.uuid != user_uuid,
    )
    print(
        "document_number:",
        data.model_dump(exclude_unset=True),
    )
    # Act / Assert
    with pytest.raises(ConflictException) as exc_info:
        service.update_user(
            user_uuid,
            data,
        )

    assert str(exc_info.value) == (
        "El correo electrónico ya está registrado."
    )

    repository.update.assert_not_called()
    db.commit.assert_not_called()


def test_update_user_document_already_exists():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    user = MagicMock()
    user.uuid = user_uuid

    existing_user = MagicMock()
    existing_user.uuid = uuid4()

    repository.get_by_uuid.return_value = user
    repository.get_by_email.return_value = None
    repository.get_by_document_number.return_value = existing_user

    data = UserUpdate(
        document_number="9999999999",
    )

    # Act / Assert
    with pytest.raises(ConflictException) as exc_info:
        service.update_user(
            user_uuid,
            data,
        )

    assert str(exc_info.value) == (
        "El documento de identidad ya está registrado."
    )

    repository.update.assert_not_called()
    db.commit.assert_not_called()


def test_delete_user_success():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    user = MagicMock()
    user.uuid = user_uuid
    user.is_active = True

    repository.get_by_uuid.return_value = user

    # Act
    result = service.delete_user(user_uuid)

    # Assert
    assert result is None

    repository.get_by_uuid.assert_called_once_with(
        user_uuid=user_uuid,
        include_inactive=False,
    )

    repository.deactivate.assert_called_once_with(user)
    db.commit.assert_called_once()


def test_activate_user_success():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    user = MagicMock()
    user.uuid = user_uuid
    user.is_active = False

    repository.get_by_uuid.return_value = user
    repository.activate.return_value = user

    # Act
    result = service.activate_user(user_uuid)

    # Assert
    assert result == user

    repository.get_by_uuid.assert_called_once_with(
        user_uuid=user_uuid,
        include_inactive=True,
    )

    repository.activate.assert_called_once_with(user)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)


def test_activate_user_already_active():
    # Arrange
    db = MagicMock()
    repository = MagicMock()

    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    user = MagicMock()
    user.uuid = user_uuid
    user.is_active = True

    repository.get_by_uuid.return_value = user

    # Act / Assert
    with pytest.raises(ConflictException) as exc_info:
        service.activate_user(user_uuid)

    assert str(exc_info.value) == (
        "El usuario ya está activo."
    )

    repository.activate.assert_not_called()
    db.commit.assert_not_called()
