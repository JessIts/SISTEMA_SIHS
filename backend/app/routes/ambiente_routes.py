from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.ambiente_controller import AmbienteController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.ambiente import (
    AmbienteCreate,
    AmbienteResponse,
    AmbienteUpdate,
)
from app.services.ambiente_service import AmbienteService


router = APIRouter(
    prefix="/ambientes",
    tags=["Ambientes"],
)


def get_ambiente_controller(
    db: Session = Depends(get_db),
) -> AmbienteController:
    service = AmbienteService(db)
    return AmbienteController(service)


@router.post(
    "",
    response_model=ApiResponse[AmbienteResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_ambiente(
    data: AmbienteCreate,
    controller: AmbienteController = Depends(
        get_ambiente_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Ambiente creado correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[AmbienteResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_ambientes(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    sede_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por sede",
    ),
    controller: AmbienteController = Depends(
        get_ambiente_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
        sede_uuid=sede_uuid,
    )

    return ApiResponse(
        message="Ambientes obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[AmbienteResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_ambientes(
    controller: AmbienteController = Depends(
        get_ambiente_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Ambientes inactivos obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/{ambiente_uuid}",
    response_model=ApiResponse[AmbienteResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_ambiente(
    ambiente_uuid: UUID,
    controller: AmbienteController = Depends(
        get_ambiente_controller
    ),
):
    item = controller.get_by_uuid(ambiente_uuid)

    return ApiResponse(
        message="Ambiente obtenido correctamente.",
        data=item,
    )


@router.put(
    "/{ambiente_uuid}",
    response_model=ApiResponse[AmbienteResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_ambiente(
    ambiente_uuid: UUID,
    data: AmbienteUpdate,
    controller: AmbienteController = Depends(
        get_ambiente_controller
    ),
):
    item = controller.update(
        ambiente_uuid,
        data,
    )

    return ApiResponse(
        message="Ambiente actualizado correctamente.",
        data=item,
    )


@router.delete(
    "/{ambiente_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva el ambiente (eliminación lógica).",
)
def delete_ambiente(
    ambiente_uuid: UUID,
    controller: AmbienteController = Depends(
        get_ambiente_controller
    ),
):
    controller.delete(ambiente_uuid)


@router.patch(
    "/{ambiente_uuid}/activate",
    response_model=ApiResponse[AmbienteResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_ambiente(
    ambiente_uuid: UUID,
    controller: AmbienteController = Depends(
        get_ambiente_controller
    ),
):
    item = controller.activate(ambiente_uuid)

    return ApiResponse(
        message="Ambiente activado correctamente.",
        data=item,
    )
