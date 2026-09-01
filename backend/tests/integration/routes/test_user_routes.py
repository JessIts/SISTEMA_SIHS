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
