from sqlalchemy import ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ResultadoAprendizaje(BaseModel):
    """La "TEMÁTICA" de cada casilla del horario."""

    __tablename__ = "resultados_aprendizaje"

    __table_args__ = (
        UniqueConstraint(
            "competencia_id",
            "codigo",
            name="uq_resultados_competencia_codigo",
        ),
    )

    competencia_id: Mapped[int] = mapped_column(
        ForeignKey("competencias.id"),
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

    competencia: Mapped["Competencia"] = relationship(
        back_populates="resultados",
        lazy="joined",
    )

    actividades: Mapped[list["ActividadAprendizaje"]] = relationship(
        back_populates="resultado",
    )
