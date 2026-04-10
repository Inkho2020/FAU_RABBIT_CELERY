"""add created at column to users table

Revision ID: 143d65e20bf0
Revises: ef310c01550f
Create Date: 2026-04-10 18:24:37.109687

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "143d65e20bf0"
down_revision: Union[str, Sequence[str], None] = "ef310c01550f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "users",
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("users", "created_at")
