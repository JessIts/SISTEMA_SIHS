from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.controllers.user_controller import UserController
from app.core.database import get_db
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
)
from app.services.user_service import UserService


router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


def get_user_controller(
    db: Session = Depends(get_db),
) -> UserController:

    service = UserService(db)

    return UserController(service)


@router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: UserCreate,
    controller: UserController = Depends(
        get_user_controller
    ),
):
    return controller.create(data)


@router.get(
    "",
    response_model=list[UserResponse],
)
def get_users(
    controller: UserController = Depends(
        get_user_controller
    ),
):
    return controller.get_all()


@router.get(
    "/inactive",
    response_model=list[UserResponse],
)
def get_inactive_users(
    controller: UserController = Depends(
        get_user_controller
    ),
):
    return controller.get_inactive()


@router.patch(
    "/{user_uuid}/activate",
    response_model=UserResponse,
)
def activate_user(
    user_uuid: UUID,
    controller: UserController = Depends(
        get_user_controller
    ),
):
    return controller.activate(user_uuid)


@router.get(
    "/{user_uuid}",
    response_model=UserResponse,
)
def get_user(
    user_uuid: UUID,
    controller: UserController = Depends(
        get_user_controller
    ),
):
    return controller.get_by_uuid(user_uuid)


@router.put(
    "/{user_uuid}",
    response_model=UserResponse,
)
def update_user(
    user_uuid: UUID,
    data: UserUpdate,
    controller: UserController = Depends(
        get_user_controller
    ),
):
    return controller.update(
        user_uuid,
        data,
    )


@router.delete(
    "/{user_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_user(
    user_uuid: UUID,
    controller: UserController = Depends(
        get_user_controller
    ),
):
    controller.delete(user_uuid)

