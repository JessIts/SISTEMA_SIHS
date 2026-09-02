from datetime import datetime, timezone
import jwt

from app.core.config import settings
from app.models.user import User

def test_login_success(client, db):
    response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Login",
            "email": "login@example.com",
            "phone": "3001234567",
            "document_number": "LOGIN-001",
            "password": "Password123!",
        },
    )

    assert response.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "login@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["access_token"]
    assert data["data"]["token_type"] == "bearer"
    
def test_login_invalid_password(client):
    client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Password",
            "email": "wrong-password@example.com",
            "phone": "3001234567",
            "document_number": "LOGIN-002",
            "password": "Password123!",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "wrong-password@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Credenciales inválidas."
    
def test_login_user_not_found(client):
    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "does-not-exist@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Credenciales inválidas."
    
def test_login_inactive_user(client, db):
    create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Inactivo",
            "email": "inactive@example.com",
            "phone": "3001234567",
            "document_number": "LOGIN-003",
            "password": "Password123!",
        },
    )

    assert create_response.status_code == 201

    user_uuid = create_response.json()["data"]["uuid"]

    user = db.query(User).filter(
        User.uuid == user_uuid
    ).first()

    assert user is not None

    user.is_active = False
    db.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "inactive@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Usuario inactivo."

def test_login_token_contains_correct_user_uuid(client, db):
    create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario JWT",
            "email": "jwt@example.com",
            "phone": "3001234567",
            "document_number": "LOGIN-004",
            "password": "Password123!",
        },
    )

    assert create_response.status_code == 201

    user_uuid = create_response.json()["data"]["uuid"]

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "jwt@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["data"]["access_token"]

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert payload["sub"] == user_uuid

def test_login_token_can_access_my_profile(client):
    create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Token",
            "email": "token@example.com",
            "phone": "3001234567",
            "document_number": "LOGIN-005",
            "password": "Password123!",
        },
    )

    assert create_response.status_code == 201

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "token@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["data"]["access_token"]

    profile_response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert profile_response.status_code == 200

    data = profile_response.json()

    assert data["data"]["email"] == "token@example.com"

def test_login_invalid_password_does_not_reveal_user_existence(client):
    client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Seguridad",
            "email": "security@example.com",
            "phone": "3001234567",
            "document_number": "LOGIN-006",
            "password": "Password123!",
        },
    )

    response_existing_user = client.post(
        "/api/v1/auth/login",
        json={
            "email": "security@example.com",
            "password": "WrongPassword123!",
        },
    )

    response_unknown_user = client.post(
        "/api/v1/auth/login",
        json={
            "email": "unknown-security@example.com",
            "password": "WrongPassword123!",
        },
    )

    assert response_existing_user.status_code == 401
    assert response_unknown_user.status_code == 401

    assert (
        response_existing_user.json()["message"]
        == response_unknown_user.json()["message"]
        == "Credenciales inválidas."
    )

def test_login_inactive_user_does_not_return_access_token(client, db):
    create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Inactivo Token",
            "email": "inactive-token@example.com",
            "phone": "3001234567",
            "document_number": "LOGIN-007",
            "password": "Password123!",
        },
    )

    assert create_response.status_code == 201

    user_uuid = create_response.json()["data"]["uuid"]

    user = (
        db.query(User)
        .filter(User.uuid == user_uuid)
        .first()
    )

    assert user is not None

    user.is_active = False
    db.commit()

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "inactive-token@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 401

    data = response.json()

    assert data["success"] is False
    assert "access_token" not in data.get("data", {})

def test_login_token_contains_required_claims(client):
    create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Claims",
            "email": "claims@example.com",
            "phone": "3001234567",
            "document_number": "LOGIN-008",
            "password": "Password123!",
        },
    )

    assert create_response.status_code == 201

    user_uuid = create_response.json()["data"]["uuid"]

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "claims@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["data"]["access_token"]

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    assert "sub" in payload
    assert "exp" in payload

    assert payload["sub"] == user_uuid
    assert payload["exp"] > datetime.now(timezone.utc).timestamp()

def test_login_token_has_configured_algorithm(client):
    client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Algorithm",
            "email": "algorithm@example.com",
            "phone": "3001234567",
            "document_number": "LOGIN-009",
            "password": "Password123!",
        },
    )

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "algorithm@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    token = response.json()["data"]["access_token"]

    header = jwt.get_unverified_header(token)

    assert header["alg"] == settings.jwt_algorithm

def test_login_token_expiration_is_configured_correctly(client):
    client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Expiracion",
            "email": "expiration@example.com",
            "phone": "3001234567",
            "document_number": "LOGIN-010",
            "password": "Password123!",
        },
    )

    before_login = int(datetime.now(timezone.utc).timestamp())

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "expiration@example.com",
            "password": "Password123!",
        },
    )

    assert response.status_code == 200

    after_login = int(datetime.now(timezone.utc).timestamp())

    token = response.json()["data"]["access_token"]

    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    expected_min_exp = (
        before_login
        + settings.jwt_access_token_expire_minutes * 60
    )

    expected_max_exp = (
        after_login
        + settings.jwt_access_token_expire_minutes * 60
    )

    assert expected_min_exp <= payload["exp"] <= expected_max_exp
