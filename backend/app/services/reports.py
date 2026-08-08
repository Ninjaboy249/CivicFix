import uuid

from fastapi import HTTPException, status

from app.models.report import Report, ReportStatus
from app.repositories.reports import ReportRepository
from app.schemas.report import ReportCreate, StatusUpdate


class ReportService:
    def __init__(self, repository: ReportRepository) -> None:
        self.repository = repository

    def create(self, payload: ReportCreate) -> Report:
        return self.repository.create(payload)

    def get(self, report_id: uuid.UUID) -> Report:
        report = self.repository.get(report_id)
        if report is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Report not found")
        return report

    def update_status(self, report_id: uuid.UUID, payload: StatusUpdate) -> Report:
        report = self.get(report_id)
        if report.status == ReportStatus.RESOLVED.value and payload.status != ReportStatus.RESOLVED:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Resolved reports cannot be reopened")
        if report.status == payload.status.value:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Report already has this status")
        return self.repository.update_status(report, payload.status.value)
