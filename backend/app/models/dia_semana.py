from sqlalchemy import CheckConstraint, SmallInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import BaseModel


class DiaSemana(BaseModel):
    """Cada COLUMNA del horario. numero = ISODOW (1 = lunes ... 7 = domingo)."""

    __tablename__ = "dias_semana"

    __table_args__ = (
        CheckConstraint(
            "numero BETWEEN 1 AND 7",
            name="ck_dias_semana_numero",
        ),
    )

    numero: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        unique=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(15),
        nullable=False,
        unique=True,
    )
