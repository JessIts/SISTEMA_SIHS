from sqlalchemy import (
    CheckConstraint,
    Enum as SAEnum,
    ForeignKey,
    ForeignKeyConstraint,
    String,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel
from app.models.enums import ModalidadClase, enum_values


class Horario(BaseModel):
    """
    Una fila = una CASILLA del horario:
    (ficha + trimestre) x día x franja -> temática, instructor, ambiente.

    Se elimina físicamente (DELETE real), porque una casilla desactivada
    seguiría ocupando el espacio en las reglas anti-choque.
    """

    __tablename__ = "horarios"

    __table_args__ = (
        # trimestre_id siempre coincide con el de la ficha_trimestre
        ForeignKeyConstraint(
            ["ficha_trimestre_id", "trimestre_id"],
            ["fichas_trimestre.id", "fichas_trimestre.trimestre_id"],
            name="fk_horarios_ficha_trimestre",
            ondelete="CASCADE",
        ),
        # presencial => tiene ambiente ; sincrónico => sin ambiente
        CheckConstraint(
            "(modalidad = 'presencial' AND ambiente_id IS NOT NULL) OR "
            "(modalidad = 'sincronico' AND ambiente_id IS NULL)",
            name="ck_horarios_ambiente_modalidad",
        ),
        # Reglas anti-choque
        UniqueConstraint(
            "ficha_trimestre_id",
            "dia_id",
            "franja_id",
            name="uq_horarios_ficha_celda",
        ),
        UniqueConstraint(
            "trimestre_id",
            "dia_id",
            "franja_id",
            "instructor_id",
            name="uq_horarios_instructor_celda",
        ),
        UniqueConstraint(
            "trimestre_id",
            "dia_id",
            "franja_id",
            "ambiente_id",
            name="uq_horarios_ambiente_celda",
        ),
    )

    ficha_trimestre_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True,
    )

    trimestre_id: Mapped[int] = mapped_column(
        ForeignKey("trimestres.id"),
        nullable=False,
    )

    dia_id: Mapped[int] = mapped_column(
        ForeignKey("dias_semana.id"),
        nullable=False,
    )

    franja_id: Mapped[int] = mapped_column(
        ForeignKey("franjas_horarias.id"),
        nullable=False,
    )

    resultado_id: Mapped[int] = mapped_column(
        ForeignKey("resultados_aprendizaje.id"),
        nullable=False,
    )

    instructor_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True,
    )

    modalidad: Mapped[ModalidadClase] = mapped_column(
        SAEnum(
            ModalidadClase,
            name="modalidad_clase",
            values_callable=enum_values,
        ),
        nullable=False,
    )

    ambiente_id: Mapped[int | None] = mapped_column(
        ForeignKey("ambientes.id"),
        nullable=True,
        index=True,
    )

    observacion: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    ficha_trimestre: Mapped["FichaTrimestre"] = relationship(
        back_populates="horarios",
        foreign_keys=[ficha_trimestre_id],
        lazy="joined",
        overlaps="trimestre",
    )

    trimestre: Mapped["Trimestre"] = relationship(
        foreign_keys=[trimestre_id],
        overlaps="ficha_trimestre,horarios",
    )

    dia: Mapped["DiaSemana"] = relationship(lazy="joined")

    franja: Mapped["FranjaHoraria"] = relationship(lazy="joined")

    resultado: Mapped["ResultadoAprendizaje"] = relationship(lazy="joined")

    instructor: Mapped["User"] = relationship(lazy="joined")

    ambiente: Mapped["Ambiente | None"] = relationship(lazy="joined")
