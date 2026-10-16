from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.briefs import CoordinacionBrief


class ProgramaCreate(BaseModel):
    codigo: str = Field(min_length=1, max_length=30, examples=["PRG-MERC"])
    nombre: str = Field(min_length=2, max_length=150, examples=["DESARROLLO DE PROCESOS DE MERCADEO"])
    nivel: str | None = Field(default=None, max_length=50, examples=["TECNÓLOGO"])
    coordinacion_uuid: UUID


class ProgramaUpdate(BaseModel):
    codigo: str | None = Field(default=None, min_length=1, max_length=30)
    nombre: str | None = Field(default=None, min_length=2, max_length=150)
    nivel: str | None = Field(default=None, max_length=50)
    coordinacion_uuid: UUID | None = None


class ProgramaResponse(BaseModel):
    uuid: UUID
    codigo: str
    nombre: str
    nivel: str | None
    coordinacion: CoordinacionBrief
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
