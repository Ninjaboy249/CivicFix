from openai import OpenAI

from app.config import Settings, get_settings
from app.schemas.analysis import ReportAnalysis, ReportAnalysisRequest


SYSTEM_PROMPT = """You organize resident-submitted civic maintenance reports.
Return a concise neutral title, one allowed category, and a severity based only on
the described impact and immediate safety risk. Summarize observable facts without
inventing details. List up to five specific details that would help responders; use
an empty list when the report is sufficient. Add a safety warning only when there
is a plausible immediate danger. Never claim that an authority has been notified."""


class AnalysisUnavailableError(RuntimeError):
    pass


class ReportAnalysisService:
    def __init__(self, settings: Settings, client: OpenAI | None = None) -> None:
        self.settings = settings
        self.client = client

    def analyze(self, payload: ReportAnalysisRequest) -> ReportAnalysis:
        if not self.settings.openai_api_key and self.client is None:
            raise AnalysisUnavailableError("AI analysis is not configured")

        client = self.client or OpenAI(api_key=self.settings.openai_api_key)
        try:
            response = client.responses.parse(
                model=self.settings.openai_model,
                input=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {
                        "role": "user",
                        "content": f"Location: {payload.location}\nDescription: {payload.description}",
                    },
                ],
                text_format=ReportAnalysis,
            )
        except Exception as exc:
            raise AnalysisUnavailableError("AI analysis is temporarily unavailable") from exc

        if response.output_parsed is None:
            raise AnalysisUnavailableError("AI analysis returned no usable result")
        return response.output_parsed


def get_analysis_service() -> ReportAnalysisService:
    return ReportAnalysisService(get_settings())
