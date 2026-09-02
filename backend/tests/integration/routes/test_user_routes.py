from app.models.roles import UserRole
from app.models.user import User
from uuid import uuid4
from app.schemas.user import UserUpdate
from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings

def test_create_user_success(client):

    response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Test",
            "email": "test@example.com",
            "phone": "3001234567",
            "document_number": "TEST-001",
            "password": "Password123!",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["data"]["role"] == "user"

def test_get_user_with_invalid_token(client):
    email = f"token-{uuid4()}@example.com"
    document_number = f"TOKEN-{str(uuid4())[:8]}"

    create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Token",
            "email": email,
            "phone": "3001234567",
            "document_number": document_number,
            "password": "Password123!",
        },
    )

    assert create_response.status_code == 201

    user_uuid = create_response.json()["data"]["uuid"]

    response = client.get(
        f"/api/v1/users/{user_uuid}",
        headers={
            "Authorization": "Bearer token-invalido",
        },
    )

    assert response.status_code == 401
    
def test_get_my_profile_with_valid_token(client):
    create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Autenticado",
            "email": "authenticated@example.com",
            "phone": "3001234567",
            "document_number": "AUTH-001",
            "password": "Password123!",
        },
    )

    assert create_response.status_code == 201

    user_uuid = create_response.json()["data"]["uuid"]

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "authenticated@example.com",
            "password": "Password123!",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["data"]["access_token"]

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["data"]["uuid"] == user_uuid
    assert data["data"]["email"] == "authenticated@example.com"
  
def test_get_inactive_users_forbidden_for_regular_user(client):
    create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Normal",
            "email": "normal@example.com",
            "phone": "3001234567",
            "document_number": "NORMAL-001",
            "password": "Password123!",
        },
    )

    assert create_response.status_code == 201

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "normal@example.com",
            "password": "Password123!",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["data"]["access_token"]

    response = client.get(
        "/api/v1/users/inactive",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Permisos insuficientes."
    
def test_get_inactive_users_allowed_for_admin(client, db):
    create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Administrador Test",
            "email": "admin@example.com",
            "phone": "3001234567",
            "document_number": "ADMIN-001",
            "password": "Password123!",
        },
    )

    assert create_response.status_code == 201

    user_uuid = create_response.json()["data"]["uuid"]

    user = db.query(User).filter(
        User.uuid == user_uuid
    ).first()

    user.role = UserRole.ADMIN
    db.commit()

    login_response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin@example.com",
            "password": "Password123!",
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["data"]["access_token"]

    response = client.get(
        "/api/v1/users/inactive",
        headers={
            "Authorization": f"Bearer {access_token}",
        },
    )

    assert response.status_code == 200
    
def test_get_my_profile_without_token(client):
    response = client.get(
        "/api/v1/users/me",
    )

    assert response.status_code == 401

    data = response.json()

    assert "detail" in data

def test_user_can_get_my_profile(client, user, user_token):
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["uuid"] == user["uuid"]
    assert data["data"]["email"] == user["email"]

def test_admin_can_get_my_profile(client, admin_user, admin_token):
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["uuid"] == str(admin_user.uuid)
    assert data["data"]["email"] == admin_user.email

def test_list_users_without_token(client):
    response = client.get(
        "/api/v1/users",
    )

    assert response.status_code == 401

def test_user_cannot_list_users(client, user_token):
    response = client.get(
        "/api/v1/users",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Permisos insuficientes."

def test_admin_can_list_users(client, admin_token):
    response = client.get(
        "/api/v1/users",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "data" in data

def test_get_user_without_token(client, user):
    response = client.get(
        f"/api/v1/users/{user['uuid']}",
    )

    assert response.status_code == 401

def test_user_cannot_get_user_by_uuid(client, user, user_token):
    response = client.get(
        f"/api/v1/users/{user['uuid']}",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Permisos insuficientes."

def test_admin_can_get_user_by_uuid(client, user, admin_token):
    response = client.get(
        f"/api/v1/users/{user['uuid']}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["uuid"] == user["uuid"]
    assert data["data"]["email"] == user["email"]

def test_get_inactive_users_without_token(client):
    response = client.get(
        "/api/v1/users/inactive",
    )

    assert response.status_code == 401

def test_user_cannot_get_inactive_users(client, user_token):
    response = client.get(
        "/api/v1/users/inactive",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Permisos insuficientes."

def test_admin_can_get_inactive_users(client, db, admin_token):
    create_response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Inactivo",
            "email": f"inactive-test-{uuid4()}@example.com",
            "phone": "3001234567",
            "document_number": f"I-{str(uuid4())[:8]}",
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

    response = client.get(
        "/api/v1/users/inactive",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)

    inactive_uuids = [
        inactive_user["uuid"]
        for inactive_user in data
    ]

    assert user_uuid in inactive_uuids

def test_activate_user_without_token(client, user):
    response = client.patch(
        f"/api/v1/users/{user['uuid']}/activate",
    )

    assert response.status_code == 401

def test_user_cannot_activate_user(client, user, user_token):
    response = client.patch(
        f"/api/v1/users/{user['uuid']}/activate",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Permisos insuficientes."

def test_admin_can_activate_user(client, db, user, admin_token):
    user_db = (
        db.query(User)
        .filter(User.uuid == user["uuid"])
        .first()
    )

    assert user_db is not None

    user_db.is_active = False
    db.commit()

    response = client.patch(
        f"/api/v1/users/{user['uuid']}/activate",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["uuid"] == user["uuid"]
    assert data["data"]["is_active"] is True

    db.refresh(user_db)

    assert user_db.is_active is True

def test_update_user_without_token(client, user):
    response = client.put(
        f"/api/v1/users/{user['uuid']}",
        json={
            "name": "Nombre Actualizado",
        },
    )

    assert response.status_code == 401

def test_user_cannot_update_user(client, user, user_token):
    response = client.put(
        f"/api/v1/users/{user['uuid']}",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
        json={
            "name": "Nombre No Permitido",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Permisos insuficientes."

def test_admin_can_update_user(client, user, admin_token):
    response = client.put(
        f"/api/v1/users/{user['uuid']}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "name": "Nombre Actualizado",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["data"]["uuid"] == user["uuid"]
    assert data["data"]["name"] == "Nombre Actualizado"

def test_delete_user_without_token(client, user):
    response = client.delete(
        f"/api/v1/users/{user['uuid']}",
    )

    assert response.status_code == 401

def test_user_cannot_delete_user(client, user, user_token):
    response = client.delete(
        f"/api/v1/users/{user['uuid']}",
        headers={
            "Authorization": f"Bearer {user_token}",
        },
    )

    assert response.status_code == 403

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "Permisos insuficientes."

def test_admin_can_delete_user(client, db, user, admin_token):
    response = client.delete(
        f"/api/v1/users/{user['uuid']}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 204
    assert response.content == b""

    user_db = (
        db.query(User)
        .filter(User.uuid == user["uuid"])
        .first()
    )

    assert user_db is not None
    assert user_db.is_active is False

def test_admin_role_cannot_be_changed_by_update(client, db, admin_user, admin_token,):
    response = client.put(
        f"/api/v1/users/{admin_user.uuid}",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
        json={
            "name": "Administrador Modificado",
            "role": "USER",
        },
    )

    assert response.status_code == 200

    db.refresh(admin_user)

    assert admin_user.name == "Administrador Modificado"
    assert admin_user.role == UserRole.ADMIN

def test_user_update_schema_does_not_allow_role():
    assert "role" not in UserUpdate.model_fields

def test_inactive_admin_cannot_access_with_existing_token(
    client,
    db,
    admin_user,
    admin_token,
):
    admin_user.is_active = False
    db.commit()

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {admin_token}",
        },
    )

    assert response.status_code == 401

def test_get_my_profile_with_expired_token(client): 
    expired_token = jwt.encode( 
        { 
            "sub": "00000000-0000-0000-0000-000000000001", 
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1), 
        }, 
        settings.jwt_secret_key, 
        algorithm=settings.jwt_algorithm, 
    ) 
    response = client.get( 
        "/api/v1/users/me", 
        headers={ 
            "Authorization": f"Bearer {expired_token}", 
        }, ) 
    
    assert response.status_code == 401 

def test_get_my_profile_with_invalid_signature(client): 
    
    invalid_token = jwt.encode( 
        { 
            "sub": "00000000-0000-0000-0000-000000000001", 
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5), 
        }, 
        "wrong-secret-key", 
        algorithm=settings.jwt_algorithm, 
    ) 
    response = client.get( "/api/v1/users/me", 
    headers={ 
            "Authorization": f"Bearer {invalid_token}", 
            }, 
    ) 
    assert response.status_code == 401 
    
def test_get_my_profile_with_malformed_token(client): 
    response = client.get( 
        "/api/v1/users/me", 
        headers={ 
            "Authorization": "Bearer token-completamente-invalido", 
        }, 
    ) 
    assert response.status_code == 401 
    
def test_get_my_profile_with_invalid_uuid_subject(client): 
    invalid_token = jwt.encode( 
        { 
            "sub": "esto-no-es-un-uuid", 
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5), 
        }, 
        settings.jwt_secret_key, 
        algorithm=settings.jwt_algorithm, 
    ) 
    response = client.get( 
        "/api/v1/users/me", 
        headers={ 
            "Authorization": f"Bearer {invalid_token}", 
        }, 
    ) 
    
    assert response.status_code == 401 
    
def test_get_my_profile_without_subject(client): 
    invalid_token = jwt.encode( 
        { 
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5), 
        }, 
        
        settings.jwt_secret_key, 
        algorithm=settings.jwt_algorithm, 
    ) 
    
    response = client.get( 
        "/api/v1/users/me", 
        headers={ 
            "Authorization": f"Bearer {invalid_token}", 
        }, 
    ) 
    
    assert response.status_code == 401
    
def test_get_my_profile_with_wrong_jwt_algorithm(client):
    token = jwt.encode(
        {
            "sub": "00000000-0000-0000-0000-000000000001",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.jwt_secret_key,
        algorithm="HS384",
    )

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 401

def test_get_my_profile_with_none_algorithm(client):
    payload = {
        "sub": "00000000-0000-0000-0000-000000000001",
        "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
    }

    token = jwt.encode(
        payload,
        key="",
        algorithm="none",
    )

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 401

def test_get_my_profile_with_bearer_without_token(client):
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer",
        },
    )

    assert response.status_code == 401

def test_get_my_profile_with_empty_bearer_token(client):
    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": "Bearer ",
        },
    )

    assert response.status_code == 401

def test_get_my_profile_with_token_from_another_user(client, user):
    other_user_uuid = "00000000-0000-0000-0000-000000000001"

    token = jwt.encode(
        {
            "sub": other_user_uuid,
            "exp": datetime.now(timezone.utc) + timedelta(minutes=5),
        },
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )

    response = client.get(
        "/api/v1/users/me",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 401


