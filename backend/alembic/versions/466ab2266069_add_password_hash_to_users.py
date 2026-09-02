"""add password hash and role to users

Revision ID: 466ab2266069
Revises: 4f5c1873669b
Create Date: 2026-09-02 06:41:23.991046
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "466ab2266069"
down_revision: Union[str, Sequence[str], None] = "4f5c1873669b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    # Crear el tipo ENUM de PostgreSQL para los roles
    user_role_enum = sa.Enum(
        "admin",
        "user",
        name="user_role",
    )

    user_role_enum.create(op.get_bind(), checkfirst=True)

    # Agregar password_hash
    op.add_column(
        "users",
        sa.Column(
            "password_hash",
            sa.String(length=255),
            nullable=False,
        ),
    )

    # Agregar role
    op.add_column(
        "users",
        sa.Column(
            "role",
            user_role_enum,
            server_default="user",
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.drop_column("users", "role")
    op.drop_column("users", "password_hash")

    # Eliminar el tipo ENUM
    user_role_enum = sa.Enum(
        "admin",
        "user",
        name="user_role",
    )

    user_role_enum.drop(op.get_bind(), checkfirst=True)