from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.common.responses import ApiResponse
from app.controllers.register_controller import RegisterController
from app.core.database import get_db
from app.schemas.register import RegisterRequest
from app.schemas.user import UserResponse
from app.services.register_service import RegisterService


router = APIRouter(
    prefix="/auth",
    tags=["Registration"],
)


def get_register_controller(
    db: Session = Depends(get_db),
) -> RegisterController:
    service = RegisterService(db)
    return RegisterController(service)


@router.post(
    "/register",
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
def register(
    data: RegisterRequest,
    controller: RegisterController = Depends(
        get_register_controller
    ),
):
    user = controller.register(data)

    return ApiResponse(
        message="Usuario registrado correctamente.",
        data=user,
    )