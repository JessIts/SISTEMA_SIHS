from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.briefs import ResultadoBrief


class ActividadAprendizajeCreate(BaseModel):
    resultado_uuid: UUID
    codigo: str = Field(min_length=1, max_length=50, examples=["ACT-01"])
    descripcion: str = Field(min_length=3, examples=["Taller de análisis de casos"])
    tipo: str = Field(min_length=2, max_length=50, examples=["TALLER"])
    duracion_minutos: int = Field(gt=0, examples=[120])


class ActividadAprendizajeUpdate(BaseModel):
    resultado_uuid: UUID | None = None
    codigo: str | None = Field(default=None, min_length=1, max_length=50)
    descripcion: str | None = Field(default=None, min_length=3)
    tipo: str | None = Field(default=None, min_length=2, max_length=50)
    duracion_minutos: int | None = Field(default=None, gt=0)


class ActividadAprendizajeResponse(BaseModel):
    uuid: UUID
    codigo: str
    descripcion: str
    tipo: str
    duracion_minutos: int
    resultado: ResultadoBrief
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
