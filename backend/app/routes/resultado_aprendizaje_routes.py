from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.common.pagination import PaginatedResponse
from app.common.responses import ApiResponse
from app.controllers.resultado_aprendizaje_controller import ResultadoAprendizajeController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.resultado_aprendizaje import (
    ResultadoAprendizajeCreate,
    ResultadoAprendizajeResponse,
    ResultadoAprendizajeUpdate,
)
from app.services.resultado_aprendizaje_service import ResultadoAprendizajeService


router = APIRouter(
    prefix="/resultados-aprendizaje",
    tags=["Resultados de aprendizaje"],
)


def get_resultado_aprendizaje_controller(
    db: Session = Depends(get_db),
) -> ResultadoAprendizajeController:
    service = ResultadoAprendizajeService(db)
    return ResultadoAprendizajeController(service)


@router.post(
    "",
    response_model=ApiResponse[ResultadoAprendizajeResponse],
    dependencies=[Depends(get_current_manager)],
    status_code=status.HTTP_201_CREATED,
)
def create_resultado_aprendizaje(
    data: ResultadoAprendizajeCreate,
    controller: ResultadoAprendizajeController = Depends(
        get_resultado_aprendizaje_controller
    ),
):
    item = controller.create(data)

    return ApiResponse(
        message="Resultado de aprendizaje creado correctamente.",
        data=item,
    )


@router.get(
    "",
    response_model=ApiResponse[PaginatedResponse[ResultadoAprendizajeResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_resultado_aprendizajes(
    page: int = Query(
        default=1,
        ge=1,
    ),
    limit: int = Query(
        default=10,
        ge=1,
        le=100,
    ),
    competencia_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por competencia",
    ),
    programa_uuid: UUID | None = Query(
        default=None,
        description="Filtrar por programa (todas sus competencias)",
    ),
    controller: ResultadoAprendizajeController = Depends(
        get_resultado_aprendizaje_controller
    ),
):
    items = controller.get_all(
        page,
        limit,
        competencia_uuid=competencia_uuid,
        programa_uuid=programa_uuid,
    )

    return ApiResponse(
        message="Resultados de aprendizaje obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/inactive",
    response_model=ApiResponse[list[ResultadoAprendizajeResponse]],
    dependencies=[Depends(get_current_manager)],
)
def get_inactive_resultado_aprendizajes(
    controller: ResultadoAprendizajeController = Depends(
        get_resultado_aprendizaje_controller
    ),
):
    items = controller.get_inactive()

    return ApiResponse(
        message="Resultados de aprendizaje inactivos obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/{resultado_aprendizaje_uuid}",
    response_model=ApiResponse[ResultadoAprendizajeResponse],
    dependencies=[Depends(get_current_manager)],
)
def get_resultado_aprendizaje(
    resultado_aprendizaje_uuid: UUID,
    controller: ResultadoAprendizajeController = Depends(
        get_resultado_aprendizaje_controller
    ),
):
    item = controller.get_by_uuid(resultado_aprendizaje_uuid)

    return ApiResponse(
        message="Resultado de aprendizaje obtenido correctamente.",
        data=item,
    )


@router.put(
    "/{resultado_aprendizaje_uuid}",
    response_model=ApiResponse[ResultadoAprendizajeResponse],
    dependencies=[Depends(get_current_manager)],
)
def update_resultado_aprendizaje(
    resultado_aprendizaje_uuid: UUID,
    data: ResultadoAprendizajeUpdate,
    controller: ResultadoAprendizajeController = Depends(
        get_resultado_aprendizaje_controller
    ),
):
    item = controller.update(
        resultado_aprendizaje_uuid,
        data,
    )

    return ApiResponse(
        message="Resultado de aprendizaje actualizado correctamente.",
        data=item,
    )


@router.delete(
    "/{resultado_aprendizaje_uuid}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_manager)],
    summary="Desactiva el resultado de aprendizaje (eliminación lógica).",
)
def delete_resultado_aprendizaje(
    resultado_aprendizaje_uuid: UUID,
    controller: ResultadoAprendizajeController = Depends(
        get_resultado_aprendizaje_controller
    ),
):
    controller.delete(resultado_aprendizaje_uuid)


@router.patch(
    "/{resultado_aprendizaje_uuid}/activate",
    response_model=ApiResponse[ResultadoAprendizajeResponse],
    dependencies=[Depends(get_current_manager)],
)
def activate_resultado_aprendizaje(
    resultado_aprendizaje_uuid: UUID,
    controller: ResultadoAprendizajeController = Depends(
        get_resultado_aprendizaje_controller
    ),
):
    item = controller.activate(resultado_aprendizaje_uuid)

    return ApiResponse(
        message="Resultado de aprendizaje activado correctamente.",
        data=item,
    )
