from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.horario_controller import HorarioController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.horario import (
    HorarioCreate,
    HorarioGrilla,
    HorarioResponse,
    HorarioUpdate,
)
from app.services.horario_service import HorarioService


router = APIRouter(
    prefix="/horarios",
    tags=["Horarios"],
)


def get_horario_controller(
    db: Session = Depends(get_db),
) -> HorarioController:
    service = HorarioService(db)
    return HorarioController(service)


@router.post(
    "",
    response_model=ApiResponse[HorarioResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_horario(
    data: HorarioCreate,
    controller: HorarioController = Depends(
        get_horario_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Horario creado correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[HorarioResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_horarios(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    ficha_trimestre_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por ficha-trimestre",
    ),
    trimestre_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por trimestre",
    ),
    instructor_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por instructor",
    ),
    ambiente_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por ambiente",
    ),
    dia_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por día",
    ),
    controller: HorarioController = Depends(
        get_horario_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
        ficha_trimestre_uuid=ficha_trimestre_uuid,
        trimestre_uuid=trimestre_uuid,
        instructor_uuid=instructor_uuid,
        ambiente_uuid=ambiente_uuid,
        dia_uuid=dia_uuid,
    )

    return ApiResponse(
        message="Horarios obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/{horario_uuid}",
    response_model=ApiResponse[HorarioResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_horario(
    horario_uuid: UUID,
    controller: HorarioController = Depends(
        get_horario_controller
    ),
):
    item = controller.get_by_uuid(horario_uuid)

    return ApiResponse(
        message="Horario obtenido correctamente.",
        data=item,
    )


@router.put(
    "/{horario_uuid}",
    response_model=ApiResponse[HorarioResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_horario(
    horario_uuid: UUID,
    data: HorarioUpdate,
    controller: HorarioController = Depends(
        get_horario_controller
    ),
):
    item = controller.update(
        horario_uuid,
        data,
    )

    return ApiResponse(
        message="Horario actualizado correctamente.",
        data=item,
    )


@router.delete(
    "/{horario_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Elimina definitivamente la casilla (libera el espacio).",
)
def delete_horario(
    horario_uuid: UUID,
    controller: HorarioController = Depends(
        get_horario_controller
    ),
):
    controller.delete(horario_uuid)


@router.get(
    "/grilla/{ficha_trimestre_uuid}",
    response_model=ApiResponse[HorarioGrilla],
    dependencies=[Depends(get_current_manager)],
    summary="Horario de la ficha armado como el archivo (franjas x días)",
)
def get_grilla_horario(
    ficha_trimestre_uuid: UUID,
    controller: HorarioController = Depends(
        get_horario_controller
    ),
):
    grilla = controller.get_grilla(ficha_trimestre_uuid)

    return ApiResponse(
        message="Horario obtenido correctamente.",
        data=grilla,
    )
