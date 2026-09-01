from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.roles import UserRole


class UserCreate(BaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )
    email: EmailStr
    phone: str = Field(
        min_length=7,
        max_length=20,
    )
    document_number: str = Field(
        min_length=5,
        max_length=30,
    )
    password: str = Field(
        min_length=8,
        max_length=128,
    )


class UserUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )
    email: EmailStr | None = None
    phone: str | None = Field(
        default=None,
        min_length=7,
        max_length=20,
    )
    document_number: str | None = Field(
        default=None,
        min_length=5,
        max_length=30,
    )
    password: str | None = Field(
        default=None,
        min_length=8,
        max_length=128,
    )


class UserResponse(BaseModel):
    uuid: UUID
    name: str
    email: EmailStr
    phone: str
    document_number: str
    role: UserRole
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class UserPagination(BaseModel):
    items: list[UserResponse]
    page: int
    limit: int
    total: int
    pages: int