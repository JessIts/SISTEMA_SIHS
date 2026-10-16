from datetime import datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.schemas.briefs import JornadaBrief


class FranjaHorariaCreate(BaseModel):
    jornada_uuid: UUID
    hora_inicio: time = Field(examples=["12:00"])
    hora_fin: time = Field(examples=["15:00"])
    orden: int = Field(ge=1, le=999, examples=[3], description="Posición de la fila en el horario.")

    @model_validator(mode="after")
    def validar_horas(self):
        if self.hora_fin <= self.hora_inicio:
            raise ValueError("La hora de fin debe ser mayor que la hora de inicio.")
        return self


class FranjaHorariaUpdate(BaseModel):
    jornada_uuid: UUID | None = None
    hora_inicio: time | None = None
    hora_fin: time | None = None
    orden: int | None = Field(default=None, ge=1, le=999)


class FranjaHorariaResponse(BaseModel):
    uuid: UUID
    hora_inicio: time
    hora_fin: time
    orden: int
    jornada: JornadaBrief
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
