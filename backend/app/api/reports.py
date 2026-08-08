import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.repositories.reports import ReportRepository
from app.schemas.report import ReportCreate, ReportResponse, StatusUpdate
from app.services.reports import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])
DbSession = Annotated[Session, Depends(get_db)]


@router.post("", response_model=ReportResponse, status_code=status.HTTP_201_CREATED)
def create_report(payload: ReportCreate, db: DbSession) -> ReportResponse:
    return ReportService(ReportRepository(db)).create(payload)


@router.get("", response_model=list[ReportResponse])
def list_reports(db: DbSession) -> list[ReportResponse]:
    return ReportRepository(db).list()


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(report_id: uuid.UUID, db: DbSession) -> ReportResponse:
    return ReportService(ReportRepository(db)).get(report_id)


@router.patch("/{report_id}/status", response_model=ReportResponse)
def update_report_status(report_id: uuid.UUID, payload: StatusUpdate, db: DbSession) -> ReportResponse:
    return ReportService(ReportRepository(db)).update_status(report_id, payload)
