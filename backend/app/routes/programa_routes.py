from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.programa_controller import ProgramaController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.programa import (
    ProgramaCreate,
    ProgramaResponse,
    ProgramaUpdate,
)
from app.services.programa_service import ProgramaService


router = APIRouter(
    prefix="/programas",
    tags=["Programas"],
)


def get_programa_controller(
    db: Session = Depends(get_db),
) -> ProgramaController:
    service = ProgramaService(db)
    return ProgramaController(service)


@router.post(
    "",
    response_model=ApiResponse[ProgramaResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_programa(
    data: ProgramaCreate,
    controller: ProgramaController = Depends(
        get_programa_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Programa creado correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[ProgramaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_programas(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    coordinacion_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por coordinación",
    ),
    controller: ProgramaController = Depends(
        get_programa_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
        coordinacion_uuid=coordinacion_uuid,
    )

    return ApiResponse(
        message="Programas obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[ProgramaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_programas(
    controller: ProgramaController = Depends(
        get_programa_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Programas inactivos obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/{programa_uuid}",
    response_model=ApiResponse[ProgramaResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_programa(
    programa_uuid: UUID,
    controller: ProgramaController = Depends(
        get_programa_controller
    ),
):
    item = controller.get_by_uuid(programa_uuid)

    return ApiResponse(
        message="Programa obtenido correctamente.",
        data=item,
    )


@router.put(
    "/{programa_uuid}",
    response_model=ApiResponse[ProgramaResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_programa(
    programa_uuid: UUID,
    data: ProgramaUpdate,
    controller: ProgramaController = Depends(
        get_programa_controller
    ),
):
    item = controller.update(
        programa_uuid,
        data,
    )

    return ApiResponse(
        message="Programa actualizado correctamente.",
        data=item,
    )


@router.delete(
    "/{programa_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva el programa (eliminación lógica).",
)
def delete_programa(
    programa_uuid: UUID,
    controller: ProgramaController = Depends(
        get_programa_controller
    ),
):
    controller.delete(programa_uuid)


@router.patch(
    "/{programa_uuid}/activate",
    response_model=ApiResponse[ProgramaResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_programa(
    programa_uuid: UUID,
    controller: ProgramaController = Depends(
        get_programa_controller
    ),
):
    item = controller.activate(programa_uuid)

    return ApiResponse(
        message="Programa activado correctamente.",
        data=item,
    )
