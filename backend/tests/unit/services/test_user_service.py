import pytest

from unittest.mock import MagicMock
from uuid import uuid4
from app.models.roles import UserRole

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
    )
from app.core.security import (
    hash_password,
    verify_password,
    )
from app.schemas.user import (
    UserCreate,
    UserUpdate,
    )
from app.services.user_service import UserService
from sqlalchemy.exc import IntegrityError


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
        password="Password123!",
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

    # La contraseña nunca debe almacenarse en texto plano
    assert user.password_hash != "Password123!"
    assert user.password_hash

    # La contraseña original debe poder verificarse contra el hash
    assert verify_password(
        "Password123!",
        user.password_hash,
    )

    repository.create.assert_called_once_with(user)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)

def test_create_user_assigns_user_role():

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
        password="Password123!",
    )

    repository.get_by_email.return_value = None
    repository.get_by_document_number.return_value = None
    repository.create.side_effect = lambda user: user

    # Act
    user = service.create_user(data)

    # Assert
    assert user.role == UserRole.USER
    assert user.role.value == "user"

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
        password="Password123!",
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
        password="Password123!",
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

def test_update_user_password_success():
    # Arrange
    db = MagicMock()
    repository = MagicMock()
    service = UserService(db)
    service.repository = repository


    user_uuid = uuid4()

    old_password = "OldPassword123!"
    new_password = "NewPassword456!"

    user = MagicMock()
    user.uuid = user_uuid
    user.password_hash = hash_password(old_password)

    repository.get_by_uuid.return_value = user
    repository.update.return_value = user

    data = UserUpdate(
        password=new_password,
    )

    # Act
    result = service.update_user(
        user_uuid,
        data,
    )

    # Assert
    assert result == user

    # Nunca debe guardarse en texto plano
    assert user.password_hash != new_password

    # El hash debe haber cambiado
    assert not verify_password(
        old_password,
        user.password_hash,
    )

    # La nueva contraseña debe funcionar
    assert verify_password(
        new_password,
        user.password_hash,
    )

    repository.update.assert_called_once_with(user)
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)

def test_update_user_password_wrong_password_fails():
    # Arrange
    db = MagicMock()
    repository = MagicMock()
    service = UserService(db)
    service.repository = repository


    user_uuid = uuid4()

    old_password = "OldPassword123!"
    new_password = "NewPassword456!"

    user = MagicMock()
    user.uuid = user_uuid
    user.password_hash = hash_password(old_password)

    repository.get_by_uuid.return_value = user
    repository.update.return_value = user

    data = UserUpdate(
        password=new_password,
    )

    # Act
    service.update_user(
        user_uuid,
        data,
    )

    # Assert
    assert not verify_password(
        "WrongPassword999!",
        user.password_hash,
    )

    assert verify_password(
        new_password,
        user.password_hash,
    )

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

def test_get_users_success():
    # Arrange
    db = MagicMock()
    repository = MagicMock()
    service = UserService(db)
    service.repository = repository


    users = [
        MagicMock(name="User 1"),
        MagicMock(name="User 2"),
    ]

    repository.get_all.return_value = (
        users,
        25,
    )

    # Act
    result = service.get_users(
        page=2,
        limit=10,
    )

    # Assert
    assert result["items"] == users
    assert result["page"] == 2
    assert result["limit"] == 10
    assert result["total"] == 25
    assert result["pages"] == 3

    repository.get_all.assert_called_once_with(
        page=2,
        limit=10,
        include_inactive=False,
    )

def test_get_users_empty():
    # Arrange
    db = MagicMock()
    repository = MagicMock()
    service = UserService(db)
    service.repository = repository


    repository.get_all.return_value = (
        [],
        0,
    )

    # Act
    result = service.get_users(
        page=1,
        limit=10,
    )

    # Assert
    assert result["items"] == []
    assert result["page"] == 1
    assert result["limit"] == 10
    assert result["total"] == 0
    assert result["pages"] == 0

    repository.get_all.assert_called_once_with(
        page=1,
        limit=10,
        include_inactive=False,
    )
    
def test_promote_user_to_admin_success():
    # Arrange
    db = MagicMock()
    repository = MagicMock()
    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    user = MagicMock()
    user.uuid = user_uuid
    user.role = UserRole.USER

    repository.get_by_uuid.return_value = user

    # Act
    result = service.promote_to_admin(user_uuid)

    # Assert
    assert result == user
    assert user.role == UserRole.ADMIN
    assert user.role.value == "admin"

    repository.get_by_uuid.assert_called_once_with(
        user_uuid=user_uuid,
        include_inactive=True,
    )
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)
    
def test_promote_user_to_admin_not_found():
    # Arrange
    db = MagicMock()
    repository = MagicMock()
    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()
    repository.get_by_uuid.return_value = None

    # Act / Assert
    with pytest.raises(NotFoundException) as exc_info:
        service.promote_to_admin(user_uuid)

    assert str(exc_info.value) == "Usuario no encontrado."

    repository.get_by_uuid.assert_called_once_with(
        user_uuid=user_uuid,
        include_inactive=True,
    )
    db.commit.assert_not_called()
    db.refresh.assert_not_called()
    
def test_promote_user_to_admin_when_already_admin():
    # Arrange
    db = MagicMock()
    repository = MagicMock()
    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    user = MagicMock()
    user.uuid = user_uuid
    user.role = UserRole.ADMIN

    repository.get_by_uuid.return_value = user

    # Act
    result = service.promote_to_admin(user_uuid)

    # Assert
    assert result == user
    assert user.role == UserRole.ADMIN
    assert user.role.value == "admin"

    repository.get_by_uuid.assert_called_once_with(
        user_uuid=user_uuid,
        include_inactive=True,
    )
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)
    
def test_promote_inactive_user_to_admin_success():
    # Arrange
    db = MagicMock()
    repository = MagicMock()
    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    user = MagicMock()
    user.uuid = user_uuid
    user.role = UserRole.USER
    user.is_active = False

    repository.get_by_uuid.return_value = user

    # Act
    result = service.promote_to_admin(user_uuid)

    # Assert
    assert result == user
    assert user.role == UserRole.ADMIN
    assert user.is_active is False

    repository.get_by_uuid.assert_called_once_with(
        user_uuid=user_uuid,
        include_inactive=True,
    )
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(user)
    
def test_promote_user_to_admin_integrity_error():
    # Arrange
    db = MagicMock()
    repository = MagicMock()
    service = UserService(db)
    service.repository = repository

    user_uuid = uuid4()

    user = MagicMock()
    user.uuid = user_uuid
    user.role = UserRole.USER

    repository.get_by_uuid.return_value = user
    db.commit.side_effect = IntegrityError(
        "statement",
        {},
        Exception("database error"),
    )

    # Act / Assert
    with pytest.raises(ConflictException) as exc_info:
        service.promote_to_admin(user_uuid)

    assert str(exc_info.value) == (
        "No fue posible promover el usuario a administrador."
    )

    assert user.role == UserRole.ADMIN
    db.rollback.assert_called_once()
    db.refresh.assert_not_called()