from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas.analysis import ReportAnalysis, ReportAnalysisRequest
from app.services.analysis import AnalysisUnavailableError, ReportAnalysisService, get_analysis_service

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/report", response_model=ReportAnalysis)
def analyze_report(
    payload: ReportAnalysisRequest,
    service: Annotated[ReportAnalysisService, Depends(get_analysis_service)],
):
    try:
        return service.analyze(payload)
    except AnalysisUnavailableError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc
