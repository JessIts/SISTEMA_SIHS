from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.briefs import SedeBrief


class CoordinacionCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=150, examples=["Coordinación Comercio y Mercadeo"])
    sedes_uuids: list[UUID] = Field(
        default_factory=list,
        description="Sedes donde opera la coordinación (opcional).",
    )


class CoordinacionUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    sedes_uuids: list[UUID] | None = Field(
        default=None,
        description="Si se envía, REEMPLAZA la lista de sedes.",
    )


class CoordinacionResponse(BaseModel):
    uuid: UUID
    nombre: str
    sedes: list[SedeBrief]
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
