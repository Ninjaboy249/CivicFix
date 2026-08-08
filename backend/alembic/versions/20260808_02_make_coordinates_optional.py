"""Make report coordinates optional."""

from typing import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260808_02"
down_revision: str | None = "20260808_01"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    with op.batch_alter_table("reports") as batch_op:
        batch_op.alter_column("latitude", existing_type=sa.Float(), nullable=True)
        batch_op.alter_column("longitude", existing_type=sa.Float(), nullable=True)


def downgrade() -> None:
    with op.batch_alter_table("reports") as batch_op:
        batch_op.alter_column("longitude", existing_type=sa.Float(), nullable=False)
        batch_op.alter_column("latitude", existing_type=sa.Float(), nullable=False)
