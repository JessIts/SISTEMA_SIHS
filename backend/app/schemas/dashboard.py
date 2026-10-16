from uuid import UUID

from pydantic import BaseModel

from app.schemas.mi import MiTrimestre


class ConteosDashboard(BaseModel):
    sedes: int
    ambientes: int
    programas: int
    fichas: int
    trimestres: int
    horarios: int


class UsuariosPorRol(BaseModel):
    admin: int = 0
    coordinador: int = 0
    instructor: int = 0
    aprendiz: int = 0
    user: int = 0


class ProgramacionResumen(BaseModel):
    ficha_trimestre_uuid: UUID
    ficha: str
    programa: str
    trimestre_ficha: int
    trimestre: str
    horas_semanales: int
    horas_programadas: float


class DashboardResumen(BaseModel):
    conteos: ConteosDashboard
    usuarios: UsuariosPorRol
    trimestres_activos: list[MiTrimestre]
    programaciones: list[ProgramacionResumen]
