import enum
import uuid
from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, Float, Index, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class ReportStatus(str, enum.Enum):
    REPORTED = "REPORTED"
    UNDER_REVIEW = "UNDER_REVIEW"
    ASSIGNED = "ASSIGNED"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"


class ReportCategory(str, enum.Enum):
    ROAD = "ROAD"
    STREETLIGHT = "STREETLIGHT"
    GARBAGE = "GARBAGE"
    WATER = "WATER"
    INFRASTRUCTURE = "INFRASTRUCTURE"
    OTHER = "OTHER"


class ReportSeverity(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"


class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        CheckConstraint("length(description) >= 10", name="ck_reports_description_length"),
        Index("ix_reports_status_created_at", "status", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(String(160), nullable=False)
    description: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(32), index=True, nullable=False)
    severity: Mapped[str] = mapped_column(String(16), index=True, nullable=False)
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(32), index=True, default=ReportStatus.REPORTED.value)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

