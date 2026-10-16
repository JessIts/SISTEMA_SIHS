from datetime import date

from sqlalchemy import CheckConstraint, Column, Date, Enum as SAEnum, ForeignKey, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, BaseModel
from app.models.enums import EstadoFicha, ModalidadFicha, enum_values


# Relación N:M aprendices <-> fichas
ficha_aprendiz = Table(
    "ficha_aprendiz",
    Base.metadata,
    Column(
        "ficha_id",
        ForeignKey("fichas.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "user_id",
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Ficha(BaseModel):

    __tablename__ = "fichas"

    __table_args__ = (
        CheckConstraint(
            "fecha_fin > fecha_inicio",
            name="ck_fichas_fechas",
        ),
    )

    codigo: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    programa_id: Mapped[int] = mapped_column(
        ForeignKey("programas.id"),
        nullable=False,
        index=True,
    )

    jornada_id: Mapped[int] = mapped_column(
        ForeignKey("jornadas.id"),
        nullable=False,
        index=True,
    )

    modalidad: Mapped[ModalidadFicha] = mapped_column(
        SAEnum(
            ModalidadFicha,
            name="modalidad_ficha",
            values_callable=enum_values,
        ),
        nullable=False,
        default=ModalidadFicha.PRESENCIAL,
        server_default=ModalidadFicha.PRESENCIAL.value,
    )

    fecha_inicio: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    fecha_fin: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    estado: Mapped[EstadoFicha] = mapped_column(
        SAEnum(
            EstadoFicha,
            name="estado_ficha",
            values_callable=enum_values,
        ),
        nullable=False,
        default=EstadoFicha.EN_FORMACION,
        server_default=EstadoFicha.EN_FORMACION.value,
    )

    programa: Mapped["Programa"] = relationship(
        back_populates="fichas",
        lazy="joined",
    )

    jornada: Mapped["Jornada"] = relationship(
        back_populates="fichas",
        lazy="joined",
    )

    aprendices: Mapped[list["User"]] = relationship(
        secondary=ficha_aprendiz,
        order_by="User.name",
    )

    fichas_trimestre: Mapped[list["FichaTrimestre"]] = relationship(
        back_populates="ficha",
    )
