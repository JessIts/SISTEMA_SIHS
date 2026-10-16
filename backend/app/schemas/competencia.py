from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.briefs import ProgramaBrief


class CompetenciaCreate(BaseModel):
    programa_uuid: UUID
    codigo: str = Field(min_length=1, max_length=50, examples=["COMP-01"])
    descripcion: str = Field(min_length=3, examples=["Gestionar el plan de mercadeo"])


class CompetenciaUpdate(BaseModel):
    programa_uuid: UUID | None = None
    codigo: str | None = Field(default=None, min_length=1, max_length=50)
    descripcion: str | None = Field(default=None, min_length=3)


class CompetenciaResponse(BaseModel):
    uuid: UUID
    codigo: str
    descripcion: str
    programa: ProgramaBrief
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
