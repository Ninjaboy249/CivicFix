from pydantic import BaseModel, Field

from app.models.report import ReportCategory, ReportSeverity


class ReportAnalysisRequest(BaseModel):
    description: str = Field(min_length=10, max_length=5000)
    location: str = Field(min_length=3, max_length=500)


class ReportAnalysis(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    category: ReportCategory
    severity: ReportSeverity
    summary: str = Field(min_length=10, max_length=1000)
    missing_information: list[str] = Field(max_length=5)
    safety_warning: str | None = Field(default=None, max_length=500)
