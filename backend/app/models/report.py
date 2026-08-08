import enum
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReportStatus(str, enum.Enum):
    REPORTED = "reported"
    UNDER_REVIEW = "under_review"
    ASSIGNED = "assigned"
    IN_PROGRESS = "in_progress"
    RESOLVED = "resolved"


class ReportCategory(str, enum.Enum):
    ROAD = "road"
    STREETLIGHT = "streetlight"
    WASTE = "waste"
    WATER = "water"
    INFRASTRUCTURE = "infrastructure"
    OTHER = "other"


class ReportSeverity(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        CheckConstraint("length(description) >= 10", name="ck_reports_description_length"),
        Index("ix_reports_status_created_at", "status", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str | None] = mapped_column(String(160), nullable=True)
    description: Mapped[str] = mapped_column(Text)
    location: Mapped[str] = mapped_column(String(500))
    category: Mapped[str | None] = mapped_column(String(32), index=True, nullable=True)
    severity: Mapped[str | None] = mapped_column(String(16), index=True, nullable=True)
    status: Mapped[str] = mapped_column(String(32), index=True, default=ReportStatus.REPORTED.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    status_history: Mapped[list["ReportStatusHistory"]] = relationship(
        back_populates="report", cascade="all, delete-orphan", order_by="ReportStatusHistory.created_at"
    )


class ReportStatusHistory(Base):
    __tablename__ = "report_status_history"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    report_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"), index=True)
    status: Mapped[str] = mapped_column(String(32))
    note: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    report: Mapped[Report] = relationship(back_populates="status_history")

