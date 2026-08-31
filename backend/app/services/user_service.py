from uuid import UUID

from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate


class UserService:

    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def create_user(
        self,
        data: UserCreate,
    ) -> User:

        existing_email = self.repository.get_by_email(
            data.email
        )

        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El correo electrónico ya está registrado.",
            )

        existing_document = (
            self.repository.get_by_document_number(
                data.document_number
            )
        )

        if existing_document:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El documento de identidad ya está registrado.",
            )

        user = User(
            name=data.name,
            email=data.email,
            phone=data.phone,
            document_number=data.document_number,
        )

        try:
            return self.repository.create(user)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No fue posible crear el usuario.",
            )

    def get_user(
        self,
        user_uuid: UUID,
    ) -> User:

        user = self.repository.get_by_uuid(
            user_uuid=user_uuid,
            include_inactive=False,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado.",
            )

        return user

    def get_users(self) -> list[User]:

        return self.repository.get_all(
            include_inactive=False,
        )

    def get_inactive_users(self) -> list[User]:

        return self.repository.get_inactive()

    def update_user(
        self,
        user_uuid: UUID,
        data: UserUpdate,
    ) -> User:

        user = self.get_user(user_uuid)

        update_data = data.model_dump(
            exclude_unset=True
        )

        if "email" in update_data:

            existing_email = self.repository.get_by_email(
                update_data["email"]
            )

            if (
                existing_email
                and existing_email.uuid != user_uuid
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="El correo electrónico ya está registrado.",
                )

        for field, value in update_data.items():
            setattr(user, field, value)

        try:
            return self.repository.update(user)

        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="No fue posible actualizar el usuario.",
            )

    def delete_user(
        self,
        user_uuid: UUID,
    ) -> None:

        user = self.get_user(user_uuid)

        self.repository.deactivate(user)

    def activate_user(
        self,
        user_uuid: UUID,
    ) -> User:

        user = self.repository.get_by_uuid(
            user_uuid=user_uuid,
            include_inactive=True,
        )

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado.",
            )

        if user.is_active:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El usuario ya está activo.",
            )

        self.repository.activate(user)

        return user
