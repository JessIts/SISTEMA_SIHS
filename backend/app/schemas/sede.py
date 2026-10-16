from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class SedeCreate(BaseModel):
    nombre: str = Field(min_length=2, max_length=150, examples=["Sede Fontibón"])
    direccion: str = Field(min_length=3, max_length=255, examples=["Cl 19A # 96c-40"])
    tipo: str = Field(default="SECUNDARIA", max_length=50, examples=["SECUNDARIA"])


class SedeUpdate(BaseModel):
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    direccion: str | None = Field(default=None, min_length=3, max_length=255)
    tipo: str | None = Field(default=None, max_length=50)


class SedeResponse(BaseModel):
    uuid: UUID
    nombre: str
    direccion: str
    tipo: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
