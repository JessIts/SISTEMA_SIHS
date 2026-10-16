from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Programa(BaseModel):

    __tablename__ = "programas"

    codigo: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
    )

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    nivel: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    coordinacion_id: Mapped[int] = mapped_column(
        ForeignKey("coordinaciones.id"),
        nullable=False,
        index=True,
    )

    coordinacion: Mapped["Coordinacion"] = relationship(
        back_populates="programas",
        lazy="joined",
    )

    competencias: Mapped[list["Competencia"]] = relationship(
        back_populates="programa",
    )

    fichas: Mapped[list["Ficha"]] = relationship(
        back_populates="programa",
    )
