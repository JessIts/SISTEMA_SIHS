from uuid import uuid4
from unittest.mock import MagicMock

from app.models.user import User
from app.repositories.user_repository import UserRepository


def test_create_user():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    user = User(
        name="Angel Gomez",
        email="angel@example.com",
        phone="3001234567",
        document_number="1234567890",
    )

    # Act
    result = repository.create(user)

    # Assert
    assert result is user
    db.add.assert_called_once_with(user)


def test_get_by_uuid_active_user():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    user_uuid = uuid4()
    user = MagicMock()
    user.uuid = user_uuid

    db.scalar.return_value = user

    # Act
    result = repository.get_by_uuid(user_uuid)

    # Assert
    assert result is user

    db.scalar.assert_called_once()


def test_get_by_uuid_include_inactive():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    user_uuid = uuid4()
    user = MagicMock()
    user.uuid = user_uuid

    db.scalar.return_value = user

    # Act
    result = repository.get_by_uuid(
        user_uuid,
        include_inactive=True,
    )

    # Assert
    assert result is user
    db.scalar.assert_called_once()


def test_get_by_email():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    user = MagicMock()
    db.scalar.return_value = user

    # Act
    result = repository.get_by_email(
        "angel@example.com"
    )

    # Assert
    assert result is user
    db.scalar.assert_called_once()


def test_get_by_document_number():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    user = MagicMock()
    db.scalar.return_value = user

    # Act
    result = repository.get_by_document_number(
        "1234567890"
    )

    # Assert
    assert result is user
    db.scalar.assert_called_once()


def test_get_all_paginated():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    users = [
        MagicMock(),
        MagicMock(),
    ]

    scalars_result = MagicMock()
    scalars_result.all.return_value = users

    db.scalar.return_value = 25
    db.scalars.return_value = scalars_result

    # Act
    result_users, total = repository.get_all(
        page=2,
        limit=10,
    )

    # Assert
    assert result_users == users
    assert total == 25

    db.scalar.assert_called_once()
    db.scalars.assert_called_once()


def test_get_all_include_inactive():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    users = [MagicMock()]

    scalars_result = MagicMock()
    scalars_result.all.return_value = users

    db.scalar.return_value = 30
    db.scalars.return_value = scalars_result

    # Act
    result_users, total = repository.get_all(
        page=1,
        limit=10,
        include_inactive=True,
    )

    # Assert
    assert result_users == users
    assert total == 30


def test_get_inactive():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    users = [
        MagicMock(),
        MagicMock(),
    ]

    scalars_result = MagicMock()
    scalars_result.all.return_value = users

    db.scalars.return_value = scalars_result

    # Act
    result = repository.get_inactive()

    # Assert
    assert result == users
    db.scalars.assert_called_once()


def test_update_user():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    user = MagicMock()

    # Act
    result = repository.update(user)

    # Assert
    assert result is user


def test_deactivate_user():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    user = MagicMock()
    user.is_active = True

    # Act
    result = repository.deactivate(user)

    # Assert
    assert result is user
    assert user.is_active is False


def test_activate_user():
    # Arrange
    db = MagicMock()
    repository = UserRepository(db)

    user = MagicMock()
    user.is_active = False

    # Act
    result = repository.activate(user)

    # Assert
    assert result is user
    assert user.is_active is True