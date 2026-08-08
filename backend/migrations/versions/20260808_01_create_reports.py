"""Create reports and status history tables."""

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
        sa.Column("title", sa.String(length=160), nullable=True),
        sa.Column("description", sa.Text(), nullable=False),
        sa.Column("location", sa.String(length=500), nullable=False),
        sa.Column("category", sa.String(length=32), nullable=True),
        sa.Column("severity", sa.String(length=16), nullable=True),
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
    op.create_table(
        "report_status_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("report_id", sa.Uuid(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("note", sa.String(length=500), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["report_id"], ["reports.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_report_status_history_report_id", "report_status_history", ["report_id"])


def downgrade() -> None:
    op.drop_index("ix_report_status_history_report_id", table_name="report_status_history")
    op.drop_table("report_status_history")
    op.drop_index("ix_reports_status_created_at", table_name="reports")
    op.drop_index("ix_reports_status", table_name="reports")
    op.drop_index("ix_reports_severity", table_name="reports")
    op.drop_index("ix_reports_category", table_name="reports")
    op.drop_table("reports")
