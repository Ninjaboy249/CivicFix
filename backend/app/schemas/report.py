import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.report import ReportCategory, ReportSeverity, ReportStatus


class ReportCreate(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    description: str = Field(min_length=10, max_length=5000)
    category: ReportCategory
    severity: ReportSeverity
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class StatusUpdate(BaseModel):
    status: ReportStatus


class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    title: str
    description: str
    category: ReportCategory
    severity: ReportSeverity
    latitude: float | None
    longitude: float | None
    status: ReportStatus
    created_at: datetime
    updated_at: datetime
