from uuid import UUID

from app.core.exceptions import ConflictException, NotFoundException, ValidationException
from app.models.ficha import Ficha
from app.models.jornada import Jornada
from app.models.programa import Programa
from app.models.roles import UserRole
from app.models.user import User
from app.repositories.ficha_repository import FichaRepository
from app.repositories.jornada_repository import JornadaRepository
from app.repositories.programa_repository import ProgramaRepository
from app.repositories.user_repository import UserRepository
from app.schemas.ficha import FichaCreate
from app.services.base_service import BaseService


class FichaService(BaseService[Ficha]):

    repository_class = FichaRepository
    entity_label = "ficha"
    female = True

    constraint_messages = {
        "fichas_codigo_key": "Ya existe una ficha con ese código.",
        "ck_fichas_fechas": "La fecha de fin debe ser posterior a la fecha de inicio.",
    }

    dependents = [
        ("fichas_trimestre", "No se puede desactivar la ficha: tiene trimestres programados activos."),
    ]

    def _programa(self, programa_uuid: UUID) -> Programa:
        return self.resolve(
            ProgramaRepository,
            programa_uuid,
            "El programa indicado no existe o está inactivo.",
        )

    def _jornada(self, jornada_uuid: UUID) -> Jornada:
        return self.resolve(
            JornadaRepository,
            jornada_uuid,
            "La jornada indicada no existe o está inactiva.",
        )

    def build_conditions(
        self,
        codigo: str | None = None,
        programa_uuid: UUID | None = None,
        jornada_uuid: UUID | None = None,
    ) -> list:
        conditions = []

        if codigo:
            conditions.append(Ficha.codigo == codigo)

        if programa_uuid:
            conditions.append(Ficha.programa.has(Programa.uuid == programa_uuid))

        if jornada_uuid:
            conditions.append(Ficha.jornada.has(Jornada.uuid == jornada_uuid))

        return conditions

    def build_entity(self, data: FichaCreate) -> Ficha:
        values = data.model_dump(exclude={"programa_uuid", "jornada_uuid"})

        return Ficha(
            **values,
            programa=self._programa(data.programa_uuid),
            jornada=self._jornada(data.jornada_uuid),
        )

    def apply_update(self, entity: Ficha, update_data: dict) -> None:
        if "programa_uuid" in update_data:
            entity.programa = self._programa(update_data.pop("programa_uuid"))

        if "jornada_uuid" in update_data:
            entity.jornada = self._jornada(update_data.pop("jornada_uuid"))

        super().apply_update(entity, update_data)

    # ------------------------------------------------------------------
    # Aprendices de la ficha (relación N:M con users)
    # ------------------------------------------------------------------
    def get_aprendices(self, ficha_uuid: UUID) -> list[User]:
        return self.get(ficha_uuid).aprendices

    def add_aprendiz(self, ficha_uuid: UUID, user_uuid: UUID) -> list[User]:
        ficha = self.get(ficha_uuid)

        user = UserRepository(self.db).get_by_uuid(
            user_uuid=user_uuid,
            include_inactive=False,
        )

        if not user:
            raise NotFoundException("Usuario no encontrado.")

        if user.role != UserRole.APRENDIZ:
            raise ValidationException(
                "Solo se pueden asociar usuarios con rol aprendiz."
            )

        if user in ficha.aprendices:
            raise ConflictException("El aprendiz ya pertenece a la ficha.")

        ficha.aprendices.append(user)

        self._commit(ficha, "No fue posible asociar el aprendiz.")

        return ficha.aprendices

    def remove_aprendiz(self, ficha_uuid: UUID, user_uuid: UUID) -> None:
        ficha = self.get(ficha_uuid)

        user = next(
            (u for u in ficha.aprendices if u.uuid == user_uuid),
            None,
        )

        if not user:
            raise NotFoundException("El aprendiz no pertenece a la ficha.")

        ficha.aprendices.remove(user)

        self._commit(None, "No fue posible quitar el aprendiz.")
