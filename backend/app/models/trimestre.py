from datetime import date

from sqlalchemy import CheckConstraint, Date, Enum as SAEnum, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.enums import EstadoTrimestre, enum_values


class Trimestre(BaseModel):
    """Periodo de CALENDARIO (2026-T3). No pertenece a ninguna ficha."""

    __tablename__ = "trimestres"

    __table_args__ = (
        UniqueConstraint(
            "anio",
            "numero",
            name="uq_trimestres_anio_numero",
        ),
        CheckConstraint(
            "numero BETWEEN 1 AND 4",
            name="ck_trimestres_numero",
        ),
        CheckConstraint(
            "fecha_fin > fecha_inicio",
            name="ck_trimestres_fechas",
        ),
    )

    anio: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    numero: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    fecha_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    fecha_fin: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    estado: Mapped[EstadoTrimestre] = mapped_column(
        SAEnum(
            EstadoTrimestre,
            name="estado_trimestre",
            values_callable=enum_values,
        ),
        nullable=False,
        default=EstadoTrimestre.PLANEACION,
        server_default=EstadoTrimestre.PLANEACION.value,
    )

    fichas_trimestre: Mapped[list["FichaTrimestre"]] = relationship(
        back_populates="trimestre",
    )
