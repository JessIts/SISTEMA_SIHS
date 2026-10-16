from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class DiaSemanaCreate(BaseModel):
    numero: int = Field(ge=1, le=7, examples=[1], description="1 = lunes ... 7 = domingo")
    nombre: str = Field(min_length=3, max_length=15, examples=["LUNES"])


class DiaSemanaUpdate(BaseModel):
    numero: int | None = Field(default=None, ge=1, le=7)
    nombre: str | None = Field(default=None, min_length=3, max_length=15)


class DiaSemanaResponse(BaseModel):
    uuid: UUID
    numero: int
    nombre: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
