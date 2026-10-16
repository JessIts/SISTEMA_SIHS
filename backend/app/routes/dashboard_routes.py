from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.common.responses import ApiResponse
from app.controllers.dashboard_controller import DashboardController
from app.core.database import get_db
from app.core.dependencies import get_current_manager
from app.schemas.dashboard import DashboardResumen
from app.services.dashboard_service import DashboardService


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


def get_dashboard_controller(
    db: Session = Depends(get_db),
) -> DashboardController:
    service = DashboardService(db)
    return DashboardController(service)


@router.get(
    "/resumen",
    response_model=ApiResponse[DashboardResumen],
    dependencies=[Depends(get_current_manager)],
)
def get_resumen(
    controller: DashboardController = Depends(
        get_dashboard_controller
    ),
):
    resumen = controller.get_resumen()

    return ApiResponse(
        message="Resumen obtenido correctamente.",
        data=resumen,
    )
