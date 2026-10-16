from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.trimestre_controller import TrimestreController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.trimestre import (
    TrimestreCreate,
    TrimestreResponse,
    TrimestreUpdate,
)
from app.services.trimestre_service import TrimestreService


router = APIRouter(
    prefix="/trimestres",
    tags=["Trimestres"],
)


def get_trimestre_controller(
    db: Session = Depends(get_db),
) -> TrimestreController:
    service = TrimestreService(db)
    return TrimestreController(service)


@router.post(
    "",
    response_model=ApiResponse[TrimestreResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_trimestre(
    data: TrimestreCreate,
    controller: TrimestreController = Depends(
        get_trimestre_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Trimestre creado correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[TrimestreResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_trimestres(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    controller: TrimestreController = Depends(
        get_trimestre_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
    )

    return ApiResponse(
        message="Trimestres obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[TrimestreResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_trimestres(
    controller: TrimestreController = Depends(
        get_trimestre_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Trimestres inactivos obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/{trimestre_uuid}",
    response_model=ApiResponse[TrimestreResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_trimestre(
    trimestre_uuid: UUID,
    controller: TrimestreController = Depends(
        get_trimestre_controller
    ),
):
    item = controller.get_by_uuid(trimestre_uuid)

    return ApiResponse(
        message="Trimestre obtenido correctamente.",
        data=item,
    )


@router.put(
    "/{trimestre_uuid}",
    response_model=ApiResponse[TrimestreResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_trimestre(
    trimestre_uuid: UUID,
    data: TrimestreUpdate,
    controller: TrimestreController = Depends(
        get_trimestre_controller
    ),
):
    item = controller.update(
        trimestre_uuid,
        data,
    )

    return ApiResponse(
        message="Trimestre actualizado correctamente.",
        data=item,
    )


@router.delete(
    "/{trimestre_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva el trimestre (eliminación lógica).",
)
def delete_trimestre(
    trimestre_uuid: UUID,
    controller: TrimestreController = Depends(
        get_trimestre_controller
    ),
):
    controller.delete(trimestre_uuid)


@router.patch(
    "/{trimestre_uuid}/activate",
    response_model=ApiResponse[TrimestreResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_trimestre(
    trimestre_uuid: UUID,
    controller: TrimestreController = Depends(
        get_trimestre_controller
    ),
):
    item = controller.activate(trimestre_uuid)

    return ApiResponse(
        message="Trimestre activado correctamente.",
        data=item,
    )
