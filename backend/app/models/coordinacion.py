from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, BaseModel


# Relación N:M "una coordinación opera en varias sedes"
coordinacion_sede = Table(
    "coordinacion_sede",
    Base.metadata,
    Column(
        "coordinacion_id",
        ForeignKey("coordinaciones.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "sede_id",
        ForeignKey("sedes.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Coordinacion(BaseModel):

    __tablename__ = "coordinaciones"

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
    )

    sedes: Mapped[list["Sede"]] = relationship(
        secondary=coordinacion_sede,
        lazy="selectin",
        order_by="Sede.nombre",
    )

    programas: Mapped[list["Programa"]] = relationship(
        back_populates="coordinacion",
    )
