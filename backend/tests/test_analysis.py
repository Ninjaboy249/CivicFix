from types import SimpleNamespace

from app.main import app
from app.schemas.analysis import ReportAnalysis
from app.services.analysis import ReportAnalysisService, get_analysis_service


PAYLOAD = {
    "description": "A deep pothole is blocking the left lane and drivers are swerving around it.",
    "location": "12 Market Street",
}


class FakeResponses:
    def __init__(self, parsed):
        self.parsed = parsed
        self.request = None

    def parse(self, **kwargs):
        self.request = kwargs
        return SimpleNamespace(output_parsed=self.parsed)


class FakeClient:
    def __init__(self, parsed):
        self.responses = FakeResponses(parsed)


def test_analyze_report_returns_valid_structured_result(client):
    result = ReportAnalysis(
        title="Deep pothole blocking Market Street lane",
        category="road",
        severity="high",
        summary="A deep pothole blocks the left lane and causes drivers to swerve.",
        missing_information=["Approximate pothole dimensions"],
        safety_warning="Keep a safe distance from moving traffic.",
    )
    fake_client = FakeClient(result)
    app.dependency_overrides[get_analysis_service] = lambda: ReportAnalysisService(
        settings=SimpleNamespace(openai_api_key="test", openai_model="test-model"),
        client=fake_client,
    )

    response = client.post("/api/analysis/report", json=PAYLOAD)

    assert response.status_code == 200
    assert response.json()["category"] == "road"
    assert fake_client.responses.request["text_format"] is ReportAnalysis
    app.dependency_overrides.pop(get_analysis_service, None)


def test_analysis_is_gracefully_unavailable_without_configuration(client):
    app.dependency_overrides[get_analysis_service] = lambda: ReportAnalysisService(
        settings=SimpleNamespace(openai_api_key=None, openai_model="test-model")
    )

    response = client.post("/api/analysis/report", json=PAYLOAD)

    assert response.status_code == 503
    assert response.json()["detail"] == "AI analysis is not configured"
    app.dependency_overrides.pop(get_analysis_service, None)


def test_analysis_validates_input_before_calling_provider(client):
    response = client.post("/api/analysis/report", json={**PAYLOAD, "description": "short"})
    assert response.status_code == 422
