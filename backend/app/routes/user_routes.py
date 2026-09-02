from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.responses import ApiResponse
from app.controllers.user_controller import UserController
from app.core.database import get_db
from app.core.dependencies import (
    get_current_admin,
    get_current_user,
)
from app.schemas.user import (
    UserCreate,
    UserPagination,
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
    response_model=ApiResponse[UserResponse],
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    data: UserCreate,
    controller: UserController = Depends(
        get_user_controller
    ),
):
    user = controller.create(data)

    return ApiResponse(
        message="Usuario creado correctamente.",
        data=user,
    )


@router.get(
    "/me",
    response_model=ApiResponse[UserResponse],
    dependencies=[Depends(get_current_user)],
)
def get_my_profile(
    current_user=Depends(get_current_user),
):
    return ApiResponse(
        message="Perfil obtenido correctamente.",
        data=current_user,
    )


@router.get(
    "",
    response_model=ApiResponse[UserPagination],
    dependencies=[Depends(get_current_admin)],
)
def get_users(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    controller: UserController = Depends(
        get_user_controller
    ),
):
    users = controller.get_all(
        page,
        limit,
    )

    return ApiResponse(
        message="Usuarios obtenidos correctamente.",
        data=users,
    )


@router.get(
    "/inactive",
    response_model=list[UserResponse],
    dependencies=[Depends(get_current_admin)],
)
def get_inactive_users(
    controller: UserController = Depends(
        get_user_controller
    ),
):
    return controller.get_inactive()


@router.get(
    "/{user_uuid}",
    response_model=ApiResponse[UserResponse],
    dependencies=[Depends(get_current_admin)],
)
def get_user(
    user_uuid: UUID,
    controller: UserController = Depends(
        get_user_controller
    ),
):
    user = controller.get_by_uuid(user_uuid)

    return ApiResponse(
        message="Usuario obtenido correctamente.",
        data=user,
    )


@router.patch(
    "/{user_uuid}/activate",
    response_model=ApiResponse[UserResponse],
    dependencies=[Depends(get_current_admin)],
)
def activate_user(
    user_uuid: UUID,
    controller: UserController = Depends(
        get_user_controller
    ),
):
    user = controller.activate(user_uuid)

    return ApiResponse(
        message="Usuario activado correctamente.",
        data=user,
    )


@router.put(
    "/{user_uuid}",
    response_model=ApiResponse[UserResponse],
    dependencies=[Depends(get_current_admin)],
)
def update_user(
    user_uuid: UUID,
    data: UserUpdate,
    controller: UserController = Depends(
        get_user_controller
    ),
):
    user = controller.update(
        user_uuid,
        data,
    )

    return ApiResponse(
        message="Usuario actualizado correctamente.",
        data=user,
    )


@router.delete(
    "/{user_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_admin)],
)
def delete_user(
    user_uuid: UUID,
    controller: UserController = Depends(
        get_user_controller
    ),
):
    controller.delete(user_uuid)

