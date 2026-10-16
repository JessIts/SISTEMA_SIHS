from app.services.dashboard_service import DashboardService


class DashboardController:

    def __init__(self, service: DashboardService):
        self.service = service

    def get_resumen(self):
        return self.service.get_resumen()
