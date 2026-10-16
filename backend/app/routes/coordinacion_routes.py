from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.coordinacion_controller import CoordinacionController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.coordinacion import (
    CoordinacionCreate,
    CoordinacionResponse,
    CoordinacionUpdate,
)
from app.services.coordinacion_service import CoordinacionService


router = APIRouter(
    prefix="/coordinaciones",
    tags=["Coordinaciones"],
)


def get_coordinacion_controller(
    db: Session = Depends(get_db),
) -> CoordinacionController:
    service = CoordinacionService(db)
    return CoordinacionController(service)


@router.post(
    "",
    response_model=ApiResponse[CoordinacionResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_coordinacion(
    data: CoordinacionCreate,
    controller: CoordinacionController = Depends(
        get_coordinacion_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Coordinación creada correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[CoordinacionResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_coordinacions(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    controller: CoordinacionController = Depends(
        get_coordinacion_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
    )

    return ApiResponse(
        message="Coordinaciones obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[CoordinacionResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_coordinacions(
    controller: CoordinacionController = Depends(
        get_coordinacion_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Coordinaciones inactivas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/{coordinacion_uuid}",
    response_model=ApiResponse[CoordinacionResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_coordinacion(
    coordinacion_uuid: UUID,
    controller: CoordinacionController = Depends(
        get_coordinacion_controller
    ),
):
    item = controller.get_by_uuid(coordinacion_uuid)

    return ApiResponse(
        message="Coordinación obtenida correctamente.",
        data=item,
    )


@router.put(
    "/{coordinacion_uuid}",
    response_model=ApiResponse[CoordinacionResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_coordinacion(
    coordinacion_uuid: UUID,
    data: CoordinacionUpdate,
    controller: CoordinacionController = Depends(
        get_coordinacion_controller
    ),
):
    item = controller.update(
        coordinacion_uuid,
        data,
    )

    return ApiResponse(
        message="Coordinación actualizada correctamente.",
        data=item,
    )


@router.delete(
    "/{coordinacion_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva la coordinación (eliminación lógica).",
)
def delete_coordinacion(
    coordinacion_uuid: UUID,
    controller: CoordinacionController = Depends(
        get_coordinacion_controller
    ),
):
    controller.delete(coordinacion_uuid)


@router.patch(
    "/{coordinacion_uuid}/activate",
    response_model=ApiResponse[CoordinacionResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_coordinacion(
    coordinacion_uuid: UUID,
    controller: CoordinacionController = Depends(
        get_coordinacion_controller
    ),
):
    item = controller.activate(coordinacion_uuid)

    return ApiResponse(
        message="Coordinación activada correctamente.",
        data=item,
    )


@router.post(
    "/{coordinacion_uuid}/sedes/{sede_uuid}",
    response_model=ApiResponse[CoordinacionResponse],
    dependencies=[Depends(get_current_manager)],
)
def add_sede_to_coordinacion(
    coordinacion_uuid: UUID,
    sede_uuid: UUID,
    controller: CoordinacionController = Depends(
        get_coordinacion_controller
    ),
):
    item = controller.add_sede(coordinacion_uuid, sede_uuid)

    return ApiResponse(
        message="Sede asociada correctamente.",
        data=item,
    )


@router.delete(
    "/{coordinacion_uuid}/sedes/{sede_uuid}",
    response_model=ApiResponse[CoordinacionResponse],
    dependencies=[Depends(get_current_manager)],
)
def remove_sede_from_coordinacion(
    coordinacion_uuid: UUID,
    sede_uuid: UUID,
    controller: CoordinacionController = Depends(
        get_coordinacion_controller
    ),
):
    item = controller.remove_sede(coordinacion_uuid, sede_uuid)

    return ApiResponse(
        message="Sede retirada correctamente.",
        data=item,
    )
