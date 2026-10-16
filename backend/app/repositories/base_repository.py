from typing import Any, Generic, TypeVar
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.base import BaseModel


ModelT = TypeVar("ModelT", bound=BaseModel)


class BaseRepository(Generic[ModelT]):
    """
    Operaciones comunes de acceso a datos (mismo estilo que UserRepository).
    Cada repositorio concreto solo define `model` y, si hace falta, el orden
    por defecto o consultas propias.
    """

    model: type[ModelT]

    def __init__(self, db: Session):
        self.db = db

    def default_order(self) -> list[Any]:
        return [self.model.id]

    def create(self, entity: ModelT) -> ModelT:
        self.db.add(entity)

        return entity

    def get_by_uuid(
        self,
        entity_uuid: UUID,
        include_inactive: bool = False,
    ) -> ModelT | None:

        statement = select(self.model).where(
            self.model.uuid == entity_uuid
        )

        if not include_inactive:
            statement = statement.where(
                self.model.is_active.is_(True)
            )

        return self.db.scalar(statement)

    def get_one_by(self, *conditions) -> ModelT | None:

        statement = select(self.model).where(*conditions)

        return self.db.scalar(statement)

    def get_all(
        self,
        page: int,
        limit: int,
        include_inactive: bool = False,
        conditions: list | None = None,
    ) -> tuple[list[ModelT], int]:

        statement = select(self.model)

        count_statement = select(
            func.count()
        ).select_from(self.model)

        filters = list(conditions or [])

        if not include_inactive:
            filters.append(
                self.model.is_active.is_(True)
            )

        if filters:
            statement = statement.where(*filters)
            count_statement = count_statement.where(*filters)

        total = self.db.scalar(count_statement) or 0

        offset = (page - 1) * limit

        statement = (
            statement
            .order_by(*self.default_order())
            .offset(offset)
            .limit(limit)
        )

        items = list(
            self.db.scalars(statement).unique().all()
        )

        return items, total

    def get_inactive(self) -> list[ModelT]:

        statement = (
            select(self.model)
            .where(self.model.is_active.is_(False))
            .order_by(*self.default_order())
        )

        return list(
            self.db.scalars(statement).unique().all()
        )

    def update(self, entity: ModelT) -> ModelT:
        return entity

    def deactivate(self, entity: ModelT) -> ModelT:
        entity.is_active = False

        return entity

    def activate(self, entity: ModelT) -> ModelT:
        entity.is_active = True

        return entity

    def delete(self, entity: ModelT) -> None:
        self.db.delete(entity)
