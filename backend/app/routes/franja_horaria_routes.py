from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.franja_horaria_controller import FranjaHorariaController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.franja_horaria import (
    FranjaHorariaCreate,
    FranjaHorariaResponse,
    FranjaHorariaUpdate,
)
from app.services.franja_horaria_service import FranjaHorariaService


router = APIRouter(
    prefix="/franjas-horarias",
    tags=["Franjas horarias"],
)


def get_franja_horaria_controller(
    db: Session = Depends(get_db),
) -> FranjaHorariaController:
    service = FranjaHorariaService(db)
    return FranjaHorariaController(service)


@router.post(
    "",
    response_model=ApiResponse[FranjaHorariaResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_franja_horaria(
    data: FranjaHorariaCreate,
    controller: FranjaHorariaController = Depends(
        get_franja_horaria_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Franja horaria creada correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[FranjaHorariaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_franja_horarias(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    jornada_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por jornada",
    ),
    controller: FranjaHorariaController = Depends(
        get_franja_horaria_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
        jornada_uuid=jornada_uuid,
    )

    return ApiResponse(
        message="Franjas horarias obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[FranjaHorariaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_franja_horarias(
    controller: FranjaHorariaController = Depends(
        get_franja_horaria_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Franjas horarias inactivas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/{franja_horaria_uuid}",
    response_model=ApiResponse[FranjaHorariaResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_franja_horaria(
    franja_horaria_uuid: UUID,
    controller: FranjaHorariaController = Depends(
        get_franja_horaria_controller
    ),
):
    item = controller.get_by_uuid(franja_horaria_uuid)

    return ApiResponse(
        message="Franja horaria obtenida correctamente.",
        data=item,
    )


@router.put(
    "/{franja_horaria_uuid}",
    response_model=ApiResponse[FranjaHorariaResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_franja_horaria(
    franja_horaria_uuid: UUID,
    data: FranjaHorariaUpdate,
    controller: FranjaHorariaController = Depends(
        get_franja_horaria_controller
    ),
):
    item = controller.update(
        franja_horaria_uuid,
        data,
    )

    return ApiResponse(
        message="Franja horaria actualizada correctamente.",
        data=item,
    )


@router.delete(
    "/{franja_horaria_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva la franja horaria (eliminación lógica).",
)
def delete_franja_horaria(
    franja_horaria_uuid: UUID,
    controller: FranjaHorariaController = Depends(
        get_franja_horaria_controller
    ),
):
    controller.delete(franja_horaria_uuid)


@router.patch(
    "/{franja_horaria_uuid}/activate",
    response_model=ApiResponse[FranjaHorariaResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_franja_horaria(
    franja_horaria_uuid: UUID,
    controller: FranjaHorariaController = Depends(
        get_franja_horaria_controller
    ),
):
    item = controller.activate(franja_horaria_uuid)

    return ApiResponse(
        message="Franja horaria activada correctamente.",
        data=item,
    )
