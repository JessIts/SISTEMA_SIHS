from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Sede(BaseModel):

    __tablename__ = "sedes"

    nombre: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
        unique=True,
    )

    direccion: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="SECUNDARIA",
        server_default="SECUNDARIA",
    )

    ambientes: Mapped[list["Ambiente"]] = relationship(
        back_populates="sede",
    )
