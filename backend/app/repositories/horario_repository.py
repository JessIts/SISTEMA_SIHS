from sqlalchemy import select

from app.models.dia_semana import DiaSemana
from app.models.franja_horaria import FranjaHoraria
from app.models.horario import Horario
from app.repositories.base_repository import BaseRepository


class HorarioRepository(BaseRepository[Horario]):

    model = Horario

    def default_order(self) -> list:
        return [Horario.id]

    def find_conflict(
        self,
        *conditions,
        exclude_id: int | None = None,
    ) -> Horario | None:
        """Busca otra casilla que choque (misma franja/día) con las condiciones dadas."""

        statement = select(Horario).where(*conditions)

        if exclude_id is not None:
            statement = statement.where(Horario.id != exclude_id)

        return self.db.scalars(statement).unique().first()

    def get_by_ficha_trimestre(
        self,
        ficha_trimestre_id: int,
    ) -> list[Horario]:

        statement = (
            select(Horario)
            .join(Horario.dia)
            .join(Horario.franja)
            .where(Horario.ficha_trimestre_id == ficha_trimestre_id)
            .order_by(FranjaHoraria.orden, DiaSemana.numero)
        )

        return list(self.db.scalars(statement).unique().all())
