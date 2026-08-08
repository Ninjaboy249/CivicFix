import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.report import ReportCategory, ReportSeverity, ReportStatus


class ReportCreate(BaseModel):
    description: str = Field(min_length=10, max_length=5000)
    location: str = Field(min_length=3, max_length=500)
    title: str | None = Field(default=None, min_length=3, max_length=160)
    category: ReportCategory | None = None
    severity: ReportSeverity | None = None


class StatusUpdate(BaseModel):
    status: ReportStatus
    note: str | None = Field(default=None, max_length=500)


class StatusHistoryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    status: ReportStatus
    note: str | None
    created_at: datetime


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str | None
    description: str
    location: str
    category: ReportCategory | None
    severity: ReportSeverity | None
    status: ReportStatus
    created_at: datetime
    updated_at: datetime


class ReportDetailResponse(ReportResponse):
    status_history: list[StatusHistoryResponse]


class ReportListResponse(BaseModel):
    items: list[ReportResponse]
    total: int
    limit: int
    offset: int

