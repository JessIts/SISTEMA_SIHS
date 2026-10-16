from sqlalchemy import CheckConstraint, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class ActividadAprendizaje(BaseModel):

    __tablename__ = "actividades_aprendizaje"

    __table_args__ = (
        UniqueConstraint(
            "resultado_id",
            "codigo",
            name="uq_actividades_resultado_codigo",
        ),
        CheckConstraint(
            "duracion_minutos > 0",
            name="ck_actividades_duracion",
        ),
    )

    resultado_id: Mapped[int] = mapped_column(
        ForeignKey("resultados_aprendizaje.id"),
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

    tipo: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    duracion_minutos: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    resultado: Mapped["ResultadoAprendizaje"] = relationship(
        back_populates="actividades",
        lazy="joined",
    )
