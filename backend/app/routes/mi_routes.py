from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.common.responses import ApiResponse
from app.controllers.mi_controller import MiController
from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.schemas.horario import HorarioGrilla
from app.schemas.mi import MiAgenda, MiFicha, MiPrograma
from app.services.mi_service import MiService


router = APIRouter(
    prefix="/mi",
    tags=["Mi información"],
)


def get_mi_controller(
    db: Session = Depends(get_db),
) -> MiController:
    service = MiService(db)
    return MiController(service)


@router.get(
    "/fichas",
    response_model=ApiResponse[list[MiFicha]],
    summary="Fichas del aprendiz o del instructor autenticado",
)
def get_mis_fichas(
    current_user=Depends(get_current_user),
    controller: MiController = Depends(
        get_mi_controller
    ),
):
    items = controller.get_mis_fichas(current_user)

    return ApiResponse(
        message="Fichas obtenidas correctamente.",
        data=items,
    )


@router.get(
    "/programas",
    response_model=ApiResponse[list[MiPrograma]],
    summary="Programas (con competencias y resultados) del usuario autenticado",
)
def get_mis_programas(
    current_user=Depends(get_current_user),
    controller: MiController = Depends(
        get_mi_controller
    ),
):
    items = controller.get_mis_programas(current_user)

    return ApiResponse(
        message="Programas obtenidos correctamente.",
        data=items,
    )


@router.get(
    "/agenda",
    response_model=ApiResponse[MiAgenda],
    summary="Horario personal del instructor (todas sus fichas)",
)
def get_mi_agenda(
    trimestre_uuid: UUID | None = Query(
        default=None,
        description="Por defecto: el trimestre activo más reciente.",
    ),
    current_user=Depends(get_current_user),
    controller: MiController = Depends(
        get_mi_controller
    ),
):
    agenda = controller.get_mi_agenda(current_user, trimestre_uuid)

    return ApiResponse(
        message="Agenda obtenida correctamente.",
        data=agenda,
    )


@router.get(
    "/horarios/{ficha_trimestre_uuid}",
    response_model=ApiResponse[HorarioGrilla],
    summary="Horario de una de mis fichas",
)
def get_horario_ficha(
    ficha_trimestre_uuid: UUID,
    current_user=Depends(get_current_user),
    controller: MiController = Depends(
        get_mi_controller
    ),
):
    grilla = controller.get_horario_ficha(current_user, ficha_trimestre_uuid)

    return ApiResponse(
        message="Horario obtenido correctamente.",
        data=grilla,
    )
