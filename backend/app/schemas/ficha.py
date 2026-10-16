from datetime import date, datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.enums import EstadoFicha, ModalidadFicha
from app.schemas.briefs import JornadaBrief, ProgramaBrief


class FichaCreate(BaseModel):
    codigo: str = Field(min_length=3, max_length=20, examples=["3141665"])
    programa_uuid: UUID
    jornada_uuid: UUID
    modalidad: ModalidadFicha = ModalidadFicha.PRESENCIAL
    fecha_inicio: date = Field(examples=["2024-10-01"])
    fecha_fin: date = Field(examples=["2026-12-31"])
    estado: EstadoFicha = EstadoFicha.EN_FORMACION

    @model_validator(mode="after")
    def validar_fechas(self):
        if self.fecha_fin <= self.fecha_inicio:
            raise ValueError("La fecha de fin debe ser posterior a la fecha de inicio.")
        return self


class FichaUpdate(BaseModel):
    codigo: str | None = Field(default=None, min_length=3, max_length=20)
    programa_uuid: UUID | None = None
    jornada_uuid: UUID | None = None
    modalidad: ModalidadFicha | None = None
    fecha_inicio: date | None = None
    fecha_fin: date | None = None
    estado: EstadoFicha | None = None


class FichaResponse(BaseModel):
    uuid: UUID
    codigo: str
    programa: ProgramaBrief
    jornada: JornadaBrief
    modalidad: ModalidadFicha
    fecha_inicio: date
    fecha_fin: date
    estado: EstadoFicha
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
