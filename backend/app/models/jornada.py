from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Jornada(BaseModel):
    """MAÑANA, TARDE, NOCHE."""

    __tablename__ = "jornadas"

    nombre: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        unique=True,
    )

    franjas: Mapped[list["FranjaHoraria"]] = relationship(
        back_populates="jornada",
        order_by="FranjaHoraria.orden",
    )

    fichas: Mapped[list["Ficha"]] = relationship(
        back_populates="jornada",
    )
