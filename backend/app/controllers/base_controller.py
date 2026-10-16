from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel as PydanticModel

from app.services.base_service import BaseService


ServiceT = TypeVar("ServiceT", bound=BaseService)


class BaseController(Generic[ServiceT]):
    """Mismo papel que UserController: recibe la petición ya validada y delega al servicio."""

    def __init__(self, service: ServiceT):
        self.service = service

    def create(self, data: PydanticModel):
        return self.service.create(data)

    def get_all(
        self,
        page: int,
        limit: int,
        **filters,
    ):
        return self.service.get_all_filtered(
            page=page,
            limit=limit,
            **filters,
        )

    def get_inactive(self):
        return self.service.get_inactive()

    def get_by_uuid(self, entity_uuid: UUID):
        return self.service.get(entity_uuid)

    def update(
        self,
        entity_uuid: UUID,
        data: PydanticModel,
    ):
        return self.service.update(entity_uuid, data)

    def delete(self, entity_uuid: UUID) -> None:
        self.service.delete(entity_uuid)

    def activate(self, entity_uuid: UUID):
        return self.service.activate(entity_uuid)
