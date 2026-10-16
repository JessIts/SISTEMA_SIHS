from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.actividad_aprendizaje_controller import ActividadAprendizajeController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.actividad_aprendizaje import (
    ActividadAprendizajeCreate,
    ActividadAprendizajeResponse,
    ActividadAprendizajeUpdate,
)
from app.services.actividad_aprendizaje_service import ActividadAprendizajeService


router = APIRouter(
    prefix="/actividades-aprendizaje",
    tags=["Actividades de aprendizaje"],
)


def get_actividad_aprendizaje_controller(
    db: Session = Depends(get_db),
) -> ActividadAprendizajeController:
    service = ActividadAprendizajeService(db)
    return ActividadAprendizajeController(service)


@router.post(
    "",
    response_model=ApiResponse[ActividadAprendizajeResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_actividad_aprendizaje(
    data: ActividadAprendizajeCreate,
    controller: ActividadAprendizajeController = Depends(
        get_actividad_aprendizaje_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Actividad de aprendizaje creada correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[ActividadAprendizajeResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_actividad_aprendizajes(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    resultado_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por resultado de aprendizaje",
    ),
    controller: ActividadAprendizajeController = Depends(
        get_actividad_aprendizaje_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
        resultado_uuid=resultado_uuid,
    )

    return ApiResponse(
        message="Actividades de aprendizaje obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[ActividadAprendizajeResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_actividad_aprendizajes(
    controller: ActividadAprendizajeController = Depends(
        get_actividad_aprendizaje_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Actividades de aprendizaje inactivas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/{actividad_aprendizaje_uuid}",
    response_model=ApiResponse[ActividadAprendizajeResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_actividad_aprendizaje(
    actividad_aprendizaje_uuid: UUID,
    controller: ActividadAprendizajeController = Depends(
        get_actividad_aprendizaje_controller
    ),
):
    item = controller.get_by_uuid(actividad_aprendizaje_uuid)

    return ApiResponse(
        message="Actividad de aprendizaje obtenida correctamente.",
        data=item,
    )


@router.put(
    "/{actividad_aprendizaje_uuid}",
    response_model=ApiResponse[ActividadAprendizajeResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_actividad_aprendizaje(
    actividad_aprendizaje_uuid: UUID,
    data: ActividadAprendizajeUpdate,
    controller: ActividadAprendizajeController = Depends(
        get_actividad_aprendizaje_controller
    ),
):
    item = controller.update(
        actividad_aprendizaje_uuid,
        data,
    )

    return ApiResponse(
        message="Actividad de aprendizaje actualizada correctamente.",
        data=item,
    )


@router.delete(
    "/{actividad_aprendizaje_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva la actividad de aprendizaje (eliminación lógica).",
)
def delete_actividad_aprendizaje(
    actividad_aprendizaje_uuid: UUID,
    controller: ActividadAprendizajeController = Depends(
        get_actividad_aprendizaje_controller
    ),
):
    controller.delete(actividad_aprendizaje_uuid)


@router.patch(
    "/{actividad_aprendizaje_uuid}/activate",
    response_model=ApiResponse[ActividadAprendizajeResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_actividad_aprendizaje(
    actividad_aprendizaje_uuid: UUID,
    controller: ActividadAprendizajeController = Depends(
        get_actividad_aprendizaje_controller
    ),
):
    item = controller.activate(actividad_aprendizaje_uuid)

    return ApiResponse(
        message="Actividad de aprendizaje activada correctamente.",
        data=item,
    )
