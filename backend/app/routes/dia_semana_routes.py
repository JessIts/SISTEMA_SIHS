from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.dia_semana_controller import DiaSemanaController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.dia_semana import (
    DiaSemanaCreate,
    DiaSemanaResponse,
    DiaSemanaUpdate,
)
from app.services.dia_semana_service import DiaSemanaService


router = APIRouter(
    prefix="/dias-semana",
    tags=["Días de la semana"],
)


def get_dia_semana_controller(
    db: Session = Depends(get_db),
) -> DiaSemanaController:
    service = DiaSemanaService(db)
    return DiaSemanaController(service)


@router.post(
    "",
    response_model=ApiResponse[DiaSemanaResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_dia_semana(
    data: DiaSemanaCreate,
    controller: DiaSemanaController = Depends(
        get_dia_semana_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Día creado correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[DiaSemanaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_dia_semanas(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    controller: DiaSemanaController = Depends(
        get_dia_semana_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
    )

    return ApiResponse(
        message="Días obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[DiaSemanaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_dia_semanas(
    controller: DiaSemanaController = Depends(
        get_dia_semana_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Días inactivos obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/{dia_semana_uuid}",
    response_model=ApiResponse[DiaSemanaResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_dia_semana(
    dia_semana_uuid: UUID,
    controller: DiaSemanaController = Depends(
        get_dia_semana_controller
    ),
):
    item = controller.get_by_uuid(dia_semana_uuid)

    return ApiResponse(
        message="Día obtenido correctamente.",
        data=item,
    )


@router.put(
    "/{dia_semana_uuid}",
    response_model=ApiResponse[DiaSemanaResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_dia_semana(
    dia_semana_uuid: UUID,
    data: DiaSemanaUpdate,
    controller: DiaSemanaController = Depends(
        get_dia_semana_controller
    ),
):
    item = controller.update(
        dia_semana_uuid,
        data,
    )

    return ApiResponse(
        message="Día actualizado correctamente.",
        data=item,
    )


@router.delete(
    "/{dia_semana_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva el día (eliminación lógica).",
)
def delete_dia_semana(
    dia_semana_uuid: UUID,
    controller: DiaSemanaController = Depends(
        get_dia_semana_controller
    ),
):
    controller.delete(dia_semana_uuid)


@router.patch(
    "/{dia_semana_uuid}/activate",
    response_model=ApiResponse[DiaSemanaResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_dia_semana(
    dia_semana_uuid: UUID,
    controller: DiaSemanaController = Depends(
        get_dia_semana_controller
    ),
):
    item = controller.activate(dia_semana_uuid)

    return ApiResponse(
        message="Día activado correctamente.",
        data=item,
    )
