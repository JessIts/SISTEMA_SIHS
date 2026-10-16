from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Ambiente(BaseModel):

    __tablename__ = "ambientes"

    __table_args__ = (
        UniqueConstraint(
            "sede_id",
            "nombre",
            name="uq_ambientes_sede_nombre",
        ),
        CheckConstraint(
            "capacidad IS NULL OR capacidad > 0",
            name="ck_ambientes_capacidad",
        ),
    )

    sede_id: Mapped[int] = mapped_column(
        ForeignKey("sedes.id"),
        nullable=False,
        index=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    capacidad: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    sede: Mapped["Sede"] = relationship(
        back_populates="ambientes",
        lazy="joined",
    )
