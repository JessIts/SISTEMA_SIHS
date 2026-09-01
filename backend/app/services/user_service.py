from uuid import UUID

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.exceptions import (
    ConflictException,
    NotFoundException,
)
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password
from app.models.roles import UserRole

from math import ceil

class UserService:

    def __init__(self, db: Session):
        self.db = db
        self.repository = UserRepository(db)

    def create_user(
        self,
        data: UserCreate,
    ) -> User:

        existing_email = self.repository.get_by_email(
            data.email
        )

        if existing_email:
            raise ConflictException(
                "El correo electrónico ya está registrado."
            )

        existing_document = (
            self.repository.get_by_document_number(
                data.document_number
            )
        )

        if existing_document:
            raise ConflictException(
                "El documento de identidad ya está registrado."
            )

        user = User(
            name=data.name,
            email=data.email,
            phone=data.phone,
            document_number=data.document_number,
            password_hash=hash_password(data.password),
            role=UserRole.USER,
        )

        try:
            self.repository.create(user)

            self.db.commit()
            self.db.refresh(user)

            return user

        except IntegrityError:
            self.db.rollback()

            raise ConflictException(
                "No fue posible crear el usuario."
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
            raise NotFoundException(
                "Usuario no encontrado."
            )

        return user

    def get_users(
        self,
        page: int,
        limit: int,
    ) -> dict:

        users, total = self.repository.get_all(
            page=page,
            limit=limit,
            include_inactive=False,
        )

        pages = ceil(total / limit) if total else 0

        return {
            "items": users,
            "page": page,
            "limit": limit,
            "total": total,
            "pages": pages,
        }

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

        # Validar correo electrónico
        if "email" in update_data:
            existing_email = self.repository.get_by_email(
                update_data["email"]
            )

            if (
                existing_email
                and existing_email.uuid != user_uuid
            ):
                raise ConflictException(
                    "El correo electrónico ya está registrado."
                )

        # Validar documento de identidad
        if "document_number" in update_data:
            existing_document = (
                self.repository.get_by_document_number(
                    update_data["document_number"]
                )
            )

            if (
                existing_document
                and existing_document.uuid != user_uuid
            ):
                raise ConflictException(
                    "El documento de identidad ya está registrado."
                )

        # Actualizar contraseña de forma segura
        
        new_password = update_data.pop("password", None)
        
        if new_password is not None:

            user.password_hash = hash_password(new_password)

        for field, value in update_data.items():
            setattr(user, field, value)

        try:
            self.repository.update(user)
            self.db.commit()
            self.db.refresh(user)
            return user
        except IntegrityError:
            self.db.rollback()
            raise ConflictException(
                "No fue posible actualizar el usuario."
            )

    def delete_user(
        self,
        user_uuid: UUID,
    ) -> None:

        user = self.get_user(user_uuid)

        try:
            self.repository.deactivate(user)

            self.db.commit()

        except IntegrityError:
            self.db.rollback()

            raise ConflictException(
                "No fue posible desactivar el usuario."
            )

    def activate_user(
        self,
        user_uuid: UUID,
    ) -> User:

        user = self.repository.get_by_uuid(
            user_uuid=user_uuid,
            include_inactive=True,
        )

        if not user:
            raise NotFoundException(
                "Usuario no encontrado."
            )

        if user.is_active:
            raise ConflictException(
                "El usuario ya está activo."
            )

        try:
            self.repository.activate(user)

            self.db.commit()
            self.db.refresh(user)

            return user

        except IntegrityError:
            self.db.rollback()

            raise ConflictException(
                "No fue posible activar el usuario."
            )