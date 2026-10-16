from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import EstadoTrimestre


class TrimestreCreate(BaseModel):
    anio: int = Field(ge=2000, le=2100, examples=[2026])
    numero: int = Field(ge=1, le=4, examples=[3])
    fecha_inicio: date = Field(examples=["2026-07-09"])
    fecha_fin: date = Field(examples=["2026-09-28"])
    estado: EstadoTrimestre = EstadoTrimestre.PLANEACION

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin <= self.fecha_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio.")
        return self


class TrimestreUpdate(BaseModel):
    anio: int | None = Field(default=None, ge=2000, le=2100)
    numero: int | None = Field(default=None, ge=1, le=4)
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    estado: EstadoTrimestre | None = None


class TrimestreResponse(BaseModel):
    uuid: UUID
    anio: int
    numero: int
    fecha_inicio: date
    fecha_fin: date
    estado: EstadoTrimestre
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
