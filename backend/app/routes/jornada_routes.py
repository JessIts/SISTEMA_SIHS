from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.jornada_controller import JornadaController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.jornada import (
    JornadaCreate,
    JornadaResponse,
    JornadaUpdate,
)
from app.services.jornada_service import JornadaService


router = APIRouter(
    prefix="/jornadas",
    tags=["Jornadas"],
)


def get_jornada_controller(
    db: Session = Depends(get_db),
) -> JornadaController:
    service = JornadaService(db)
    return JornadaController(service)


@router.post(
    "",
    response_model=ApiResponse[JornadaResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_jornada(
    data: JornadaCreate,
    controller: JornadaController = Depends(
        get_jornada_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Jornada creada correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[JornadaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_jornadas(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    controller: JornadaController = Depends(
        get_jornada_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
    )

    return ApiResponse(
        message="Jornadas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[JornadaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_jornadas(
    controller: JornadaController = Depends(
        get_jornada_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Jornadas inactivas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/{jornada_uuid}",
    response_model=ApiResponse[JornadaResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_jornada(
    jornada_uuid: UUID,
    controller: JornadaController = Depends(
        get_jornada_controller
    ),
):
    item = controller.get_by_uuid(jornada_uuid)

    return ApiResponse(
        message="Jornada obtenida correctamente.",
        data=item,
    )


@router.put(
    "/{jornada_uuid}",
    response_model=ApiResponse[JornadaResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_jornada(
    jornada_uuid: UUID,
    data: JornadaUpdate,
    controller: JornadaController = Depends(
        get_jornada_controller
    ),
):
    item = controller.update(
        jornada_uuid,
        data,
    )

    return ApiResponse(
        message="Jornada actualizada correctamente.",
        data=item,
    )


@router.delete(
    "/{jornada_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva la jornada (eliminación lógica).",
)
def delete_jornada(
    jornada_uuid: UUID,
    controller: JornadaController = Depends(
        get_jornada_controller
    ),
):
    controller.delete(jornada_uuid)


@router.patch(
    "/{jornada_uuid}/activate",
    response_model=ApiResponse[JornadaResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_jornada(
    jornada_uuid: UUID,
    controller: JornadaController = Depends(
        get_jornada_controller
    ),
):
    item = controller.activate(jornada_uuid)

    return ApiResponse(
        message="Jornada activada correctamente.",
        data=item,
    )
