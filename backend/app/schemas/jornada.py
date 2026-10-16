from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class JornadaCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=30, examples=["TARDE"])


class JornadaUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=30)


class JornadaResponse(BaseModel):
    uuid: UUID
    nombre: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
