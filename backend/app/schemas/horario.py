from datetime import date, datetime, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ModalidadClase
from app.schemas.briefs import (
    AmbienteBrief,
    DiaBrief,
    FichaTrimestreBrief,
    FranjaBrief,
    ResultadoBrief,
    UserBrief,
)


class HorarioCreate(BaseModel):
    ficha_trimestre_uuid: UUID
    dia_uuid: UUID
    franja_uuid: UUID
    resultado_uuid: UUID = Field(description="Temática (resultado de aprendizaje).")
    instructor_uuid: UUID = Field(description="Usuario con rol instructor.")
    modalidad: ModalidadClase = ModalidadClase.PRESENCIAL
    ambiente_uuid: UUID | None = Field(
        default=None,
        description="Obligatorio si es presencial; debe ir vacío si es sincrónico.",
    )
    observacion: str | None = Field(default=None, max_length=255)


class HorarioUpdate(BaseModel):
    dia_uuid: UUID | None = None
    franja_uuid: UUID | None = None
    resultado_uuid: UUID | None = None
    instructor_uuid: UUID | None = None
    modalidad: ModalidadClase | None = None
    ambiente_uuid: UUID | None = None
    observacion: str | None = Field(default=None, max_length=255)


class HorarioResponse(BaseModel):
    uuid: UUID
    ficha_trimestre: FichaTrimestreBrief
    dia: DiaBrief
    franja: FranjaBrief
    resultado: ResultadoBrief
    instructor: UserBrief
    modalidad: ModalidadClase
    ambiente: AmbienteBrief | None
    observacion: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ----------------------------------------------------------------------
# Grilla: el horario armado como el archivo PDF
# ----------------------------------------------------------------------
class ClaseCelda(BaseModel):
    horario_uuid: UUID
    tematica: str
    resultado_codigo: str
    instructor: str
    instructor_uuid: UUID
    modalidad: ModalidadClase
    ambiente: str


class CeldaGrilla(BaseModel):
    dia_numero: int
    dia: str
    clase: ClaseCelda | None


class FilaGrilla(BaseModel):
    franja_uuid: UUID
    hora_inicio: time
    hora_fin: time
    celdas: list[CeldaGrilla]


class JornadaGrilla(BaseModel):
    jornada: str
    franjas: list[FilaGrilla]


class EncabezadoGrilla(BaseModel):
    ficha_trimestre_uuid: UUID
    nombre_grupo: str
    ficha: str
    programa: str
    trimestre_ficha: int
    anio: int
    trimestre_anio: int
    fecha_inicio: date
    fecha_fin: date
    horas_semanales: int
    horas_programadas: float
    aprendices: int


class HorarioGrilla(BaseModel):
    encabezado: EncabezadoGrilla
    dias: list[DiaBrief]
    jornadas: list[JornadaGrilla]
