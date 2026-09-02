from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.responses import ApiResponse
from app.controllers.auth_controller import AuthController
from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


def get_auth_controller(
    db: Session = Depends(get_db),
) -> AuthController:
    service = AuthService(db)
    return AuthController(service)


@router.post(
    "/login",
    response_model=ApiResponse[TokenResponse],
)
def login(
    data: LoginRequest,
    controller: AuthController = Depends(get_auth_controller),
):
    token = controller.login(data)

    return ApiResponse(
        message="Inicio de sesión exitoso.",
        data=token,
    )