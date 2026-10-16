from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.responses import ApiResponse
from app.controllers.auth_controller import AuthController
from app.core.database import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth_service import AuthService
from fastapi import APIRouter, Depends, Response

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
)
def login(
    response: Response,
    data: LoginRequest,
    controller: AuthController = Depends(
        get_auth_controller
    ),
):
    token = controller.login(data)

    response.set_cookie(
        key="access_token",
        value=token.access_token,
        httponly=True,
        secure=False,
        samesite="lax",
        path="/",
    )

    return {
        "message": "Inicio de sesión exitoso.",
        "data": {
            "authenticated": True,
        },
    }
    
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(
        key="access_token",
        path="/",
    )

    return {
        "message": "Sesión cerrada correctamente.",
        "data": {
            "authenticated": False,
        },
    }