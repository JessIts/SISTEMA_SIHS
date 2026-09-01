def test_create_user_success(client):
    response = client.post(
        "/api/v1/users",
        json={
            "name": "Usuario Test",
            "email": "test@example.com",
            "phone": "3001234567",
            "document_number": "TEST-001",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Usuario creado correctamente."

    user = data["data"]

    assert user["name"] == "Usuario Test"
    assert user["email"] == "test@example.com"
    assert user["phone"] == "3001234567"
    assert user["document_number"] == "TEST-001"
    assert user["is_active"] is True
    assert "uuid" in user
    assert "created_at" in user