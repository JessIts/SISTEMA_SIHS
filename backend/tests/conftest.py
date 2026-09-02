import os
from uuid import uuid4

import pytest

from fastapi.testclient import TestClient

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.database import get_db
from app.main import app
from app.models.base import Base
from app.models.roles import UserRole
from app.models.user import User


TEST_DATABASE_URL = os.getenv(
    "TEST_DATABASE_URL",
    "postgresql+psycopg://postgres:admin@localhost:5433/sihs_test",
)

test_engine = create_engine(
    TEST_DATABASE_URL,
    pool_pre_ping=True,
)

TestingSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=test_engine)

    yield

    Base.metadata.drop_all(bind=test_engine)


@pytest.fixture
def db():
    session = TestingSessionLocal()

    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


@pytest.fixture
def user(client):
    email = f"user-{uuid4()}@example.com"

    response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Test",
            "email": email,
            "phone": "3001234567",
            "document_number": f"U-{str(uuid4())[:8]}",
            "password": "Password123!",
        },
    )

    assert response.status_code == 201, response.json()

    return response.json()["data"]


@pytest.fixture
def user_token(client, user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": user["email"],
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    return response.json()["data"]["access_token"]


@pytest.fixture
def admin_user(client, db):
    email = f"admin-{uuid4()}@example.com"

    response = client.post(
        "/api/v1/users",
        json={
            "name": "Administrador Test",
            "email": email,
            "phone": "3001234567",
            "document_number": f"A-{str(uuid4())[:8]}",
            "password": "Password123!",
        },
    )

    assert response.status_code == 201, response.json()

    user_uuid = response.json()["data"]["uuid"]

    admin = (
        db.query(User)
        .filter(User.uuid == user_uuid)
        .first()
    )

    assert admin is not None

    admin.role = UserRole.ADMIN
    db.commit()
    db.refresh(admin)

    return admin


@pytest.fixture
def admin_token(client, admin_user):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": admin_user.email,
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    return response.json()["data"]["access_token"]

