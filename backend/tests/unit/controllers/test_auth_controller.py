from unittest.mock import MagicMock

from app.controllers.auth_controller import AuthController
from app.schemas.auth import LoginRequest, TokenResponse


def test_login_success():
    service = MagicMock()
    controller = AuthController(service)

    service.authenticate_user.return_value = {
        "access_token": "token-de-prueba",
        "token_type": "bearer",
    }

    data = LoginRequest(
        email="angel@example.com",
        password="Password123!",
    )

    result = controller.login(data)

    assert isinstance(result, TokenResponse)
    assert result.access_token == "token-de-prueba"
    assert result.token_type == "bearer"

    service.authenticate_user.assert_called_once_with(
        email="angel@example.com",
        password="Password123!",
    )