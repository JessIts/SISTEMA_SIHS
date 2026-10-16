from datetime import time

from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger, Time, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class FranjaHoraria(BaseModel):
    """Cada FILA del horario: 06:15-09:00, 09:00-12:00, ..."""

    __tablename__ = "franjas_horarias"

    __table_args__ = (
        UniqueConstraint(
            "hora_inicio",
            "hora_fin",
            name="uq_franjas_horas",
        ),
        CheckConstraint(
            "hora_fin > hora_inicio",
            name="ck_franjas_horas",
        ),
    )

    jornada_id: Mapped[int] = mapped_column(
        ForeignKey("jornadas.id"),
        nullable=False,
        index=True,
    )

    hora_inicio: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    hora_fin: Mapped[time] = mapped_column(
        Time,
        nullable=False,
    )

    orden: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
        unique=True,
    )

    jornada: Mapped["Jornada"] = relationship(
        back_populates="franjas",
        lazy="joined",
    )
