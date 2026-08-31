from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User


class UserRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, user: User) -> User:
        self.db.add(user)

        return user

    def get_by_uuid(
        self,
        user_uuid: UUID,
        include_inactive: bool = False,
    ) -> User | None:

        statement = select(User).where(
            User.uuid == user_uuid
        )

        if not include_inactive:
            statement = statement.where(
                User.is_active.is_(True)
            )

        return self.db.scalar(statement)

    def get_by_email(
        self,
        email: str,
    ) -> User | None:

        statement = select(User).where(
            User.email == email
        )

        return self.db.scalar(statement)

    def get_by_document_number(
        self,
        document_number: str,
    ) -> User | None:

        statement = select(User).where(
            User.document_number == document_number
        )

        return self.db.scalar(statement)

    def get_all(
        self,
        include_inactive: bool = False,
    ) -> list[User]:

        statement = select(User)

        if not include_inactive:
            statement = statement.where(
                User.is_active.is_(True)
            )

        statement = statement.order_by(User.id)

        return list(
            self.db.scalars(statement).all()
        )

    def get_inactive(self) -> list[User]:

        statement = (
            select(User)
            .where(User.is_active.is_(False))
            .order_by(User.id)
        )

        return list(
            self.db.scalars(statement).all()
        )

    def update(self, user: User) -> User:
        return user

    def deactivate(self, user: User) -> User:
        user.is_active = False

        return user

    def activate(self, user: User) -> User:
        user.is_active = True

        return user
