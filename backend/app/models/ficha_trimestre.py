from sqlalchemy import CheckConstraint, ForeignKey, SmallInteger, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class FichaTrimestre(BaseModel):
    """
    Encabezado del horario: "7_TRM_3141665 ... 24 horas ... 09/07 - 28/09".
    Une una ficha con un trimestre de calendario.
    """

    __tablename__ = "fichas_trimestre"

    __table_args__ = (
        UniqueConstraint(
            "ficha_id",
            "trimestre_id",
            name="uq_fichas_trimestre_ficha_trimestre",
        ),
        UniqueConstraint(
            "ficha_id",
            "trimestre_ficha",
            name="uq_fichas_trimestre_ficha_numero",
        ),
        # Necesaria para la FK compuesta de horarios
        UniqueConstraint(
            "id",
            "trimestre_id",
            name="uq_fichas_trimestre_id_trimestre",
        ),
        CheckConstraint(
            "trimestre_ficha > 0",
            name="ck_fichas_trimestre_numero",
        ),
        CheckConstraint(
            "horas_semanales > 0",
            name="ck_fichas_trimestre_horas",
        ),
    )

    ficha_id: Mapped[int] = mapped_column(
        ForeignKey("fichas.id"),
        nullable=False,
        index=True,
    )

    trimestre_id: Mapped[int] = mapped_column(
        ForeignKey("trimestres.id"),
        nullable=False,
        index=True,
    )

    trimestre_ficha: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    horas_semanales: Mapped[int] = mapped_column(
        SmallInteger,
        nullable=False,
    )

    ficha: Mapped["Ficha"] = relationship(
        back_populates="fichas_trimestre",
        lazy="joined",
    )

    trimestre: Mapped["Trimestre"] = relationship(
        back_populates="fichas_trimestre",
        lazy="joined",
    )

    horarios: Mapped[list["Horario"]] = relationship(
        back_populates="ficha_trimestre",
        foreign_keys="Horario.ficha_trimestre_id",
        overlaps="horarios_trimestre",
    )
