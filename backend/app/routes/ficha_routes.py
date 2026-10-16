from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.ficha_controller import FichaController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.ficha import (
    FichaCreate,
    FichaResponse,
    FichaUpdate,
)
from app.schemas.user import UserResponse
from app.services.ficha_service import FichaService


router = APIRouter(
    prefix="/fichas",
    tags=["Fichas"],
)


def get_ficha_controller(
    db: Session = Depends(get_db),
) -> FichaController:
    service = FichaService(db)
    return FichaController(service)


@router.post(
    "",
    response_model=ApiResponse[FichaResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_ficha(
    data: FichaCreate,
    controller: FichaController = Depends(
        get_ficha_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Ficha creada correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[FichaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_fichas(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    codigo: str | None = Query(
        default=None,
        description="Código exacto de la ficha",
    ),
    programa_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por programa",
    ),
    jornada_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por jornada",
    ),
    controller: FichaController = Depends(
        get_ficha_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
        codigo=codigo,
        programa_uuid=programa_uuid,
        jornada_uuid=jornada_uuid,
    )

    return ApiResponse(
        message="Fichas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[FichaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_fichas(
    controller: FichaController = Depends(
        get_ficha_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Fichas inactivas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/{ficha_uuid}",
    response_model=ApiResponse[FichaResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_ficha(
    ficha_uuid: UUID,
    controller: FichaController = Depends(
        get_ficha_controller
    ),
):
    item = controller.get_by_uuid(ficha_uuid)

    return ApiResponse(
        message="Ficha obtenida correctamente.",
        data=item,
    )


@router.put(
    "/{ficha_uuid}",
    response_model=ApiResponse[FichaResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_ficha(
    ficha_uuid: UUID,
    data: FichaUpdate,
    controller: FichaController = Depends(
        get_ficha_controller
    ),
):
    item = controller.update(
        ficha_uuid,
        data,
    )

    return ApiResponse(
        message="Ficha actualizada correctamente.",
        data=item,
    )


@router.delete(
    "/{ficha_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva la ficha (eliminación lógica).",
)
def delete_ficha(
    ficha_uuid: UUID,
    controller: FichaController = Depends(
        get_ficha_controller
    ),
):
    controller.delete(ficha_uuid)


@router.patch(
    "/{ficha_uuid}/activate",
    response_model=ApiResponse[FichaResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_ficha(
    ficha_uuid: UUID,
    controller: FichaController = Depends(
        get_ficha_controller
    ),
):
    item = controller.activate(ficha_uuid)

    return ApiResponse(
        message="Ficha activada correctamente.",
        data=item,
    )


@router.get(
    "/{ficha_uuid}/aprendices",
    response_model=ApiResponse[list[UserResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_aprendices_ficha(
    ficha_uuid: UUID,
    controller: FichaController = Depends(
        get_ficha_controller
    ),
):
    items = controller.get_aprendices(ficha_uuid)

    return ApiResponse(
        message="Aprendices obtenidos correctamente.",
        data=items,
    )


@router.post(
    "/{ficha_uuid}/aprendices/{user_uuid}",
    response_model=ApiResponse[list[UserResponse]],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def add_aprendiz_ficha(
    ficha_uuid: UUID,
    user_uuid: UUID,
    controller: FichaController = Depends(
        get_ficha_controller
    ),
):
    items = controller.add_aprendiz(ficha_uuid, user_uuid)

    return ApiResponse(
        message="Aprendiz asociado correctamente.",
        data=items,
    )


@router.delete(
    "/{ficha_uuid}/aprendices/{user_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
)
def remove_aprendiz_ficha(
    ficha_uuid: UUID,
    user_uuid: UUID,
    controller: FichaController = Depends(
        get_ficha_controller
    ),
):
    controller.remove_aprendiz(ficha_uuid, user_uuid)
