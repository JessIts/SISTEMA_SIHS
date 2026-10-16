from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.briefs import CompetenciaBrief


class ResultadoAprendizajeCreate(BaseModel):
    competencia_uuid: UUID
    codigo: str = Field(min_length=1, max_length=50, examples=["15"])
    descripcion: str = Field(
        min_length=3,
        examples=["Seleccionar técnica de evaluación de estrategias para el plan de mercadeo"],
    )


class ResultadoAprendizajeUpdate(BaseModel):
    competencia_uuid: UUID | None = None
    codigo: str | None = Field(default=None, min_length=1, max_length=50)
    descripcion: str | None = Field(default=None, min_length=3)


class ResultadoAprendizajeResponse(BaseModel):
    uuid: UUID
    codigo: str
    descripcion: str
    competencia: CompetenciaBrief
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
