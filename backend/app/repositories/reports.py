import uuid

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.models.report import Report, ReportStatus, ReportStatusHistory
from app.schemas.report import ReportCreate


class ReportRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, payload: ReportCreate) -> Report:
        report = Report(**payload.model_dump(mode="json"), status=ReportStatus.REPORTED.value)
        report.status_history.append(ReportStatusHistory(status=report.status))
        self.db.add(report)
        self.db.commit()
        return self.get(report.id)  # type: ignore[return-value]

    def get(self, report_id: uuid.UUID) -> Report | None:
        statement = select(Report).options(selectinload(Report.status_history)).where(Report.id == report_id)
        return self.db.scalar(statement)

    def list(
        self,
        *,
        search: str | None,
        status: str | None,
        category: str | None,
        severity: str | None,
        limit: int,
        offset: int,
    ) -> tuple[list[Report], int]:
        filters = []
        if search:
            pattern = f"%{search}%"
            filters.append(or_(Report.title.ilike(pattern), Report.description.ilike(pattern), Report.location.ilike(pattern)))
        if status:
            filters.append(Report.status == status)
        if category:
            filters.append(Report.category == category)
        if severity:
            filters.append(Report.severity == severity)

        items = list(self.db.scalars(select(Report).where(*filters).order_by(Report.created_at.desc()).limit(limit).offset(offset)))
        total = self.db.scalar(select(func.count()).select_from(Report).where(*filters)) or 0
        return items, total

    def update_status(self, report: Report, status: str, note: str | None) -> Report:
        report.status = status
        report.status_history.append(ReportStatusHistory(status=status, note=note))
        self.db.commit()
        return self.get(report.id)  # type: ignore[return-value]
