from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.sede_controller import SedeController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.sede import (
    SedeCreate,
    SedeResponse,
    SedeUpdate,
)
from app.services.sede_service import SedeService


router = APIRouter(
    prefix="/sedes",
    tags=["Sedes"],
)


def get_sede_controller(
    db: Session = Depends(get_db),
) -> SedeController:
    service = SedeService(db)
    return SedeController(service)


@router.post(
    "",
    response_model=ApiResponse[SedeResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_sede(
    data: SedeCreate,
    controller: SedeController = Depends(
        get_sede_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Sede creada correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[SedeResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_sedes(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    controller: SedeController = Depends(
        get_sede_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
    )

    return ApiResponse(
        message="Sedes obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[SedeResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_sedes(
    controller: SedeController = Depends(
        get_sede_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Sedes inactivas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/{sede_uuid}",
    response_model=ApiResponse[SedeResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_sede(
    sede_uuid: UUID,
    controller: SedeController = Depends(
        get_sede_controller
    ),
):
    item = controller.get_by_uuid(sede_uuid)

    return ApiResponse(
        message="Sede obtenida correctamente.",
        data=item,
    )


@router.put(
    "/{sede_uuid}",
    response_model=ApiResponse[SedeResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_sede(
    sede_uuid: UUID,
    data: SedeUpdate,
    controller: SedeController = Depends(
        get_sede_controller
    ),
):
    item = controller.update(
        sede_uuid,
        data,
    )

    return ApiResponse(
        message="Sede actualizada correctamente.",
        data=item,
    )


@router.delete(
    "/{sede_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva la sede (eliminación lógica).",
)
def delete_sede(
    sede_uuid: UUID,
    controller: SedeController = Depends(
        get_sede_controller
    ),
):
    controller.delete(sede_uuid)


@router.patch(
    "/{sede_uuid}/activate",
    response_model=ApiResponse[SedeResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_sede(
    sede_uuid: UUID,
    controller: SedeController = Depends(
        get_sede_controller
    ),
):
    item = controller.activate(sede_uuid)

    return ApiResponse(
        message="Sede activada correctamente.",
        data=item,
    )
