from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.briefs import FichaBrief, TrimestreBrief


class FichaTrimestreCreate(BaseModel):
    ficha_uuid: UUID
    trimestre_uuid: UUID
    trimestre_ficha: int = Field(
        ge=1,
        le=20,
        examples=[7],
        description='Trimestre de formación en que va la ficha (el "7" de 7_TRM).',
    )
    horas_semanales: int = Field(ge=1, le=60, examples=[24])


class FichaTrimestreUpdate(BaseModel):
    trimestre_ficha: int | None = Field(default=None, ge=1, le=20)
    horas_semanales: int | None = Field(default=None, ge=1, le=60)


class FichaTrimestreResponse(BaseModel):
    uuid: UUID
    ficha: FichaBrief
    trimestre: TrimestreBrief
    trimestre_ficha: int
    horas_semanales: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
