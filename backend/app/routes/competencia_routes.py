from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.competencia_controller import CompetenciaController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.competencia import (
    CompetenciaCreate,
    CompetenciaResponse,
    CompetenciaUpdate,
)
from app.services.competencia_service import CompetenciaService


router = APIRouter(
    prefix="/competencias",
    tags=["Competencias"],
)


def get_competencia_controller(
    db: Session = Depends(get_db),
) -> CompetenciaController:
    service = CompetenciaService(db)
    return CompetenciaController(service)


@router.post(
    "",
    response_model=ApiResponse[CompetenciaResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_competencia(
    data: CompetenciaCreate,
    controller: CompetenciaController = Depends(
        get_competencia_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Competencia creada correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[CompetenciaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_competencias(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    programa_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por programa",
    ),
    controller: CompetenciaController = Depends(
        get_competencia_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
        programa_uuid=programa_uuid,
    )

    return ApiResponse(
        message="Competencias obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[CompetenciaResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_competencias(
    controller: CompetenciaController = Depends(
        get_competencia_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Competencias inactivas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/{competencia_uuid}",
    response_model=ApiResponse[CompetenciaResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_competencia(
    competencia_uuid: UUID,
    controller: CompetenciaController = Depends(
        get_competencia_controller
    ),
):
    item = controller.get_by_uuid(competencia_uuid)

    return ApiResponse(
        message="Competencia obtenida correctamente.",
        data=item,
    )


@router.put(
    "/{competencia_uuid}",
    response_model=ApiResponse[CompetenciaResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_competencia(
    competencia_uuid: UUID,
    data: CompetenciaUpdate,
    controller: CompetenciaController = Depends(
        get_competencia_controller
    ),
):
    item = controller.update(
        competencia_uuid,
        data,
    )

    return ApiResponse(
        message="Competencia actualizada correctamente.",
        data=item,
    )


@router.delete(
    "/{competencia_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva la competencia (eliminación lógica).",
)
def delete_competencia(
    competencia_uuid: UUID,
    controller: CompetenciaController = Depends(
        get_competencia_controller
    ),
):
    controller.delete(competencia_uuid)


@router.patch(
    "/{competencia_uuid}/activate",
    response_model=ApiResponse[CompetenciaResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_competencia(
    competencia_uuid: UUID,
    controller: CompetenciaController = Depends(
        get_competencia_controller
    ),
):
    item = controller.activate(competencia_uuid)

    return ApiResponse(
        message="Competencia activada correctamente.",
        data=item,
    )
