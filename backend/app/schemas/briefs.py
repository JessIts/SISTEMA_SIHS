"""
Referencias resumidas que se anidan en las respuestas.
Ej: un ambiente responde con  "sede": {"uuid": "...", "nombre": "Sede Fontibón"}
"""
from datetime import date, time
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class BriefModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    uuid: UUID


class SedeBrief(BriefModel):
    nombre: str


class AmbienteBrief(BriefModel):
    nombre: str
    sede: SedeBrief


class CoordinacionBrief(BriefModel):
    nombre: str


class ProgramaBrief(BriefModel):
    codigo: str
    nombre: str


class CompetenciaBrief(BriefModel):
    codigo: str
    descripcion: str


class ResultadoBrief(BriefModel):
    codigo: str
    descripcion: str


class JornadaBrief(BriefModel):
    nombre: str


class FranjaBrief(BriefModel):
    hora_inicio: time
    hora_fin: time


class DiaBrief(BriefModel):
    numero: int
    nombre: str


class TrimestreBrief(BriefModel):
    anio: int
    numero: int
    fecha_inicio: date
    fecha_fin: date


class FichaBrief(BriefModel):
    codigo: str


class FichaTrimestreBrief(BriefModel):
    trimestre_ficha: int
    ficha: FichaBrief
    trimestre: TrimestreBrief


class UserBrief(BriefModel):
    name: str
    document_number: str
