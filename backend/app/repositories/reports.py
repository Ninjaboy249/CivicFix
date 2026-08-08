import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.report import Report, ReportCategory, ReportSeverity, ReportStatus
from app.schemas.report import ReportCreate


class ReportRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: ReportCreate) -> Report:
        report = Report(**payload.model_dump(mode="json"), status=ReportStatus.REPORTED.value)
        self.db.add(report)
        self.db.commit()
        self.db.refresh(report)
        return report

    def get(self, report_id: uuid.UUID) -> Report | None:
        return self.db.get(Report, report_id)

    def list(
        self,
        *,
        category: ReportCategory | None = None,
        severity: ReportSeverity | None = None,
        status: ReportStatus | None = None,
    ) -> list[Report]:
        statement = select(Report)
        if category is not None:
            statement = statement.where(Report.category == category.value)
        if severity is not None:
            statement = statement.where(Report.severity == severity.value)
        if status is not None:
            statement = statement.where(Report.status == status.value)
        return list(self.db.scalars(statement.order_by(Report.created_at.desc())))

    def update_status(self, report: Report, status: str) -> Report:
        report.status = status
        self.db.commit()
        self.db.refresh(report)
        return report
