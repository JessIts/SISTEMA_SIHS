from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.ficha_trimestre_controller import FichaTrimestreController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.ficha_trimestre import (
    FichaTrimestreCreate,
    FichaTrimestreResponse,
    FichaTrimestreUpdate,
)
from app.services.ficha_trimestre_service import FichaTrimestreService


router = APIRouter(
    prefix="/fichas-trimestre",
    tags=["Fichas por trimestre"],
)


def get_ficha_trimestre_controller(
    db: Session = Depends(get_db),
) -> FichaTrimestreController:
    service = FichaTrimestreService(db)
    return FichaTrimestreController(service)


@router.post(
    "",
    response_model=ApiResponse[FichaTrimestreResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_ficha_trimestre(
    data: FichaTrimestreCreate,
    controller: FichaTrimestreController = Depends(
        get_ficha_trimestre_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Programación de ficha por trimestre creada correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[FichaTrimestreResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_ficha_trimestres(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    ficha_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por ficha",
    ),
    trimestre_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por trimestre",
    ),
    controller: FichaTrimestreController = Depends(
        get_ficha_trimestre_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
        ficha_uuid=ficha_uuid,
        trimestre_uuid=trimestre_uuid,
    )

    return ApiResponse(
        message="Programaciones de fichas por trimestre obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[FichaTrimestreResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_ficha_trimestres(
    controller: FichaTrimestreController = Depends(
        get_ficha_trimestre_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Programaciones de fichas por trimestre inactivas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/{ficha_trimestre_uuid}",
    response_model=ApiResponse[FichaTrimestreResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_ficha_trimestre(
    ficha_trimestre_uuid: UUID,
    controller: FichaTrimestreController = Depends(
        get_ficha_trimestre_controller
    ),
):
    item = controller.get_by_uuid(ficha_trimestre_uuid)

    return ApiResponse(
        message="Programación de ficha por trimestre obtenida correctamente.",
        data=item,
    )


@router.put(
    "/{ficha_trimestre_uuid}",
    response_model=ApiResponse[FichaTrimestreResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_ficha_trimestre(
    ficha_trimestre_uuid: UUID,
    data: FichaTrimestreUpdate,
    controller: FichaTrimestreController = Depends(
        get_ficha_trimestre_controller
    ),
):
    item = controller.update(
        ficha_trimestre_uuid,
        data,
    )

    return ApiResponse(
        message="Programación de ficha por trimestre actualizada correctamente.",
        data=item,
    )


@router.delete(
    "/{ficha_trimestre_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva la programación de ficha por trimestre (eliminación lógica).",
)
def delete_ficha_trimestre(
    ficha_trimestre_uuid: UUID,
    controller: FichaTrimestreController = Depends(
        get_ficha_trimestre_controller
    ),
):
    controller.delete(ficha_trimestre_uuid)


@router.patch(
    "/{ficha_trimestre_uuid}/activate",
    response_model=ApiResponse[FichaTrimestreResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_ficha_trimestre(
    ficha_trimestre_uuid: UUID,
    controller: FichaTrimestreController = Depends(
        get_ficha_trimestre_controller
    ),
):
    item = controller.activate(ficha_trimestre_uuid)

    return ApiResponse(
        message="Programación de ficha por trimestre activada correctamente.",
        data=item,
    )
