"""Create reports table."""

from typing import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "20260808_01"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "reports",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=160), nullable=False),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=False),
        sa.Column("severity", sa.String(length=16), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.CheckConstraint("length(description) >= 10", name="ck_reports_description_length"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_reports_category", "reports", ["category"])
    op.create_index("ix_reports_severity", "reports", ["severity"])
    op.create_index("ix_reports_status", "reports", ["status"])
    op.create_index("ix_reports_status_created_at", "reports", ["status", "created_at"])


def downgrade() -> None:
    op.drop_index("ix_reports_status_created_at", table_name="reports")
    op.drop_index("ix_reports_status", table_name="reports")
    op.drop_index("ix_reports_severity", table_name="reports")
    op.drop_index("ix_reports_category", table_name="reports")
    op.drop_table("reports")
