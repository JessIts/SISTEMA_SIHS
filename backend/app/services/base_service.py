from typing import Any, Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel as PydanticModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.common.pagination import build_page
from app.core.exceptions import (
    ConflictException,
    NotFoundException,
    ValidationException,
)
from app.models.base import BaseModel
from app.repositories.base_repository import BaseRepository


ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseService(Generic[ModelT]):
    """
    Lógica común de los CRUD:
      - buscar por uuid (solo activos)
      - listar paginado con filtros
      - crear / actualizar con manejo de IntegrityError
      - "eliminar" = desactivar (is_active = False), igual que en usuarios
      - reactivar

    Cada servicio concreto define:
      repository_class   -> repositorio del modelo
      entity_label       -> "sede", "programa"... (para los mensajes)
      female             -> True si el sustantivo es femenino ("la sede")
      constraint_messages-> {nombre_restricción: mensaje} para errores de BD
      dependents         -> [(relación, mensaje)] que impiden desactivar
      build_entity()     -> crea el modelo a partir del schema
      apply_update()     -> aplica los cambios (por defecto setattr)
    """

    repository_class: type[BaseRepository]
    entity_label: str = "registro"
    female: bool = False
    constraint_messages: dict[str, str] = {}
    dependents: list[tuple[str, str]] = []

    def __init__(self, db: Session):
        self.db = db
        self.repository = self.repository_class(db)

    # ------------------------------------------------------------------
    # Mensajes
    # ------------------------------------------------------------------
    @property
    def _label(self) -> str:
        return self.entity_label.capitalize()

    def _end(self) -> str:
        return "a" if self.female else "o"

    def not_found_message(self) -> str:
        return f"{self._label} no encontrad{self._end()}."

    # ------------------------------------------------------------------
    # Lectura
    # ------------------------------------------------------------------
    def get(self, entity_uuid: UUID) -> ModelT:

        entity = self.repository.get_by_uuid(
            entity_uuid=entity_uuid,
            include_inactive=False,
        )

        if not entity:
            raise NotFoundException(
                self.not_found_message()
            )

        return entity

    def get_all(
        self,
        page: int,
        limit: int,
        conditions: list | None = None,
    ) -> dict:

        items, total = self.repository.get_all(
            page=page,
            limit=limit,
            include_inactive=False,
            conditions=conditions,
        )

        return build_page(items, total, page, limit)

    def get_all_filtered(
        self,
        page: int,
        limit: int,
        **filters,
    ) -> dict:
        """Lista aplicando solo los filtros que llegaron (los None se ignoran)."""

        active_filters = {
            key: value
            for key, value in filters.items()
            if value is not None
        }

        return self.get_all(
            page=page,
            limit=limit,
            conditions=self.build_conditions(**active_filters),
        )

    def build_conditions(self, **filters) -> list:
        """Los servicios con filtros (ej. sede_uuid) lo sobrescriben."""

        return []

    def get_inactive(self) -> list[ModelT]:
        return self.repository.get_inactive()

    # ------------------------------------------------------------------
    # Escritura
    # ------------------------------------------------------------------
    def create(self, data: PydanticModel) -> ModelT:

        entity = self.build_entity(data)

        self.repository.create(entity)

        return self._commit(
            entity,
            f"No fue posible crear {self._article()} {self.entity_label}.",
        )

    def update(
        self,
        entity_uuid: UUID,
        data: PydanticModel,
    ) -> ModelT:

        entity = self.get(entity_uuid)

        update_data = data.model_dump(exclude_unset=True)

        self.apply_update(entity, update_data)

        self.repository.update(entity)

        return self._commit(
            entity,
            f"No fue posible actualizar {self._article()} {self.entity_label}.",
        )

    def delete(self, entity_uuid: UUID) -> None:

        entity = self.get(entity_uuid)

        self.validate_can_deactivate(entity)

        self.repository.deactivate(entity)

        self._commit(
            None,
            f"No fue posible desactivar {self._article()} {self.entity_label}.",
        )

    def activate(self, entity_uuid: UUID) -> ModelT:

        entity = self.repository.get_by_uuid(
            entity_uuid=entity_uuid,
            include_inactive=True,
        )

        if not entity:
            raise NotFoundException(
                self.not_found_message()
            )

        if entity.is_active:
            raise ConflictException(
                f"{self._label} ya está activ{self._end()}."
            )

        self.repository.activate(entity)

        return self._commit(
            entity,
            f"No fue posible activar {self._article()} {self.entity_label}.",
        )

    # ------------------------------------------------------------------
    # Ganchos que sobrescriben los servicios concretos
    # ------------------------------------------------------------------
    def build_entity(self, data: PydanticModel) -> ModelT:
        raise NotImplementedError

    def apply_update(
        self,
        entity: ModelT,
        update_data: dict[str, Any],
    ) -> None:

        for field, value in update_data.items():
            setattr(entity, field, value)

    def validate_can_deactivate(self, entity: ModelT) -> None:

        for relation, message in self.dependents:
            children = getattr(entity, relation)

            if any(child.is_active for child in children):
                raise ConflictException(message)

    # ------------------------------------------------------------------
    # Utilidades
    # ------------------------------------------------------------------
    def _article(self) -> str:
        return "la" if self.female else "el"

    def resolve(
        self,
        repository_class: type[BaseRepository],
        entity_uuid: UUID,
        message: str,
    ):
        """
        Convierte el uuid recibido en el body en la entidad relacionada.
        Si no existe o está inactiva -> 422 con `message`.
        """

        entity = repository_class(self.db).get_by_uuid(
            entity_uuid=entity_uuid,
            include_inactive=False,
        )

        if not entity:
            raise ValidationException(message)

        return entity

    def _commit(
        self,
        entity: ModelT | None,
        default_message: str,
    ) -> ModelT | None:

        try:
            self.db.commit()

            if entity is not None:
                self.db.refresh(entity)

            return entity

        except IntegrityError as error:
            self.db.rollback()

            raise ConflictException(
                self._integrity_message(error, default_message)
            )

    def _integrity_message(
        self,
        error: IntegrityError,
        default_message: str,
    ) -> str:

        diag = getattr(error.orig, "diag", None)

        constraint = getattr(diag, "constraint_name", None)

        if constraint and constraint in self.constraint_messages:
            return self.constraint_messages[constraint]

        return default_message
