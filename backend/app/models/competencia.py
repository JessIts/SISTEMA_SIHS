from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Competencia(BaseModel):

    __tablename__ = "competencias"

    __table_args__ = (
        UniqueConstraint(
            "programa_id",
            "codigo",
            name="uq_competencias_programa_codigo",
        ),
    )

    programa_id: Mapped[int] = mapped_column(
        ForeignKey("programas.id"),
        nullable=False,
        index=True,
    )

    codigo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    descripcion: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    programa: Mapped["Programa"] = relationship(
        back_populates="competencias",
        lazy="joined",
    )

    resultados: Mapped[list["ResultadoAprendizaje"]] = relationship(
        back_populates="competencia",
    )
