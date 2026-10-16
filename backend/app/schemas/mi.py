from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.enums import EstadoFicha, EstadoTrimestre, ModalidadClase, ModalidadFicha
from app.schemas.briefs import CoordinacionBrief, DiaBrief, JornadaBrief, ProgramaBrief


class MiTrimestre(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    anio: int
    numero: int
    fecha_inicio: date
    fecha_fin: date
    estado: EstadoTrimestre


class MiProgramacion(BaseModel):
    """Una ficha en un trimestre (permite abrir su horario)."""

    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    trimestre_ficha: int
    horas_semanales: int
    trimestre: MiTrimestre


class MiFicha(BaseModel):
    uuid: UUID
    codigo: str
    modalidad: ModalidadFicha
    estado: EstadoFicha
    fecha_inicio: date
    fecha_fin: date
    jornada: JornadaBrief
    programa: ProgramaBrief
    programaciones: list[MiProgramacion]


class MiResultado(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID
    codigo: str
    descripcion: str


class MiCompetencia(BaseModel):
    uuid: UUID
    codigo: str
    descripcion: str
    resultados: list[MiResultado]


class MiPrograma(BaseModel):
    uuid: UUID
    codigo: str
    nombre: str
    nivel: str | None
    coordinacion: CoordinacionBrief
    competencias: list[MiCompetencia]


# ----------------------------------------------------------------------
# Agenda del instructor (sus clases en todas las fichas)
# ----------------------------------------------------------------------
class ClaseAgenda(BaseModel):
    horario_uuid: UUID
    ficha: str
    ficha_trimestre_uuid: UUID
    tematica: str
    resultado_codigo: str
    modalidad: ModalidadClase
    ambiente: str


class CeldaAgenda(BaseModel):
    dia_numero: int
    dia: str
    clase: ClaseAgenda | None


class FilaAgenda(BaseModel):
    franja_uuid: UUID
    hora_inicio: time
    hora_fin: time
    celdas: list[CeldaAgenda]


class JornadaAgenda(BaseModel):
    jornada: str
    franjas: list[FilaAgenda]


class MiAgenda(BaseModel):
    trimestre: MiTrimestre | None
    trimestres: list[MiTrimestre]
    horas_programadas: float
    total_clases: int
    dias: list[DiaBrief]
    jornadas: list[JornadaAgenda]
