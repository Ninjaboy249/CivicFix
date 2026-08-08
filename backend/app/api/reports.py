import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.report import ReportCategory, ReportSeverity, ReportStatus
from app.repositories.reports import ReportRepository
from app.schemas.report import ReportCreate, ReportDetailResponse, ReportListResponse, StatusUpdate
from app.services.reports import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=ReportDetailResponse, status_code=status.HTTP_201_CREATED)
def create_report(payload: ReportCreate, db: DbSession):
    return ReportService(ReportRepository(db)).create(payload)


@router.get("", response_model=ReportListResponse)
def list_reports(
    db: DbSession,
    search: Annotated[str | None, Query(min_length=2, max_length=100)] = None,
    report_status: Annotated[ReportStatus | None, Query(alias="status")] = None,
    category: ReportCategory | None = None,
    severity: ReportSeverity | None = None,
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
):
    items, total = ReportRepository(db).list(
        search=search,
        status=report_status.value if report_status else None,
        category=category.value if category else None,
        severity=severity.value if severity else None,
        limit=limit,
        offset=offset,
    )
    return ReportListResponse(items=items, total=total, limit=limit, offset=offset)


@router.get("/{report_id}", response_model=ReportDetailResponse)
def get_report(report_id: uuid.UUID, db: DbSession):
    return ReportService(ReportRepository(db)).get(report_id)


@router.patch("/{report_id}/status", response_model=ReportDetailResponse)
def update_report_status(report_id: uuid.UUID, payload: StatusUpdate, db: DbSession):
    return ReportService(ReportRepository(db)).update_status(report_id, payload)

