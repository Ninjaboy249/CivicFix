# CivicFix

CivicFix is an AI-assisted civic issue reporting and tracking platform. It is intended to help residents create clear reports for community maintenance problems and follow each report through resolution.

> Current scope: Phase 3. Structured AI-assisted report analysis is implemented through the REST API, alongside report persistence and status tracking. Uploads, duplicate detection, authentication, and administration are not implemented yet.

## Problem being solved

Community maintenance reports are often incomplete or difficult to track. CivicFix will give residents one structured workflow for describing an issue, confirming its details, and monitoring its status without pretending to integrate with a government department that has not actually been connected.

## Architecture

```text
Browser -> Next.js frontend -> FastAPI REST API -> PostgreSQL
                                      |
                                      +-> OpenAI API (Phase 3)
```

The repository is split by responsibility:

- `frontend/`: Next.js presentation layer and accessible user interface.
- `backend/app/api/`: HTTP route definitions and validation boundaries.
- `backend/app/config.py`: environment-based backend configuration.
- `backend/app/services/`: business rules independent of HTTP handling.
- `backend/app/repositories/`: SQLAlchemy database access.
- `backend/app/models/` and `schemas/`: persistence models and API validation models.
- `backend/migrations/`: versioned Alembic schema changes.

## Technology stack

- Next.js 15, React, TypeScript, and Tailwind CSS
- FastAPI, Python 3.12, Pydantic, and Uvicorn
- PostgreSQL 18, SQLAlchemy 2, Psycopg 3, and Alembic
- Zerops service and build configuration

## Local development setup

Requirements: Node.js 20+, npm, Python 3.12+, and Git (optional).

### Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:3000`.

### Backend

In a second PowerShell window, from the repository root:

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
```

Open `http://localhost:8000/api/health`. Interactive API documentation is at `http://localhost:8000/docs`.

## Environment variables

Copy `.env.example` values into your local environment as needed. Never commit real secrets.

| Variable | Service | Purpose |
| --- | --- | --- |
| `NEXT_PUBLIC_API_URL` | frontend | Public URL used by the browser to reach the API |
| `ENVIRONMENT` | backend | Runtime name such as `development` or `production` |
| `CORS_ORIGINS` | backend | Comma-separated trusted browser origins |
| `DATABASE_URL` | backend | SQLAlchemy PostgreSQL connection URL |
| `OPENAI_API_KEY` | backend | Server-only credential for report analysis |
| `OPENAI_MODEL` | backend | Structured-output capable model; defaults to `gpt-5.6` |

The API still starts without an OpenAI credential. In that state, the analysis endpoint returns `503` while report CRUD remains available.

## Database setup

For local development, start PostgreSQL with Docker Compose and apply migrations:

```powershell
docker compose up -d db
cd backend
Copy-Item .env.example .env
.\.venv\Scripts\Activate.ps1
python -m alembic upgrade head
```

The default local credentials are intentionally development-only. Zerops supplies its managed connection string through `DATABASE_URL`; the application selects the Psycopg 3 SQLAlchemy driver without logging credentials.

Available endpoints:

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/api/reports` | Create a report and its initial timeline event |
| `GET` | `/api/reports` | Search, filter, and paginate reports |
| `GET` | `/api/reports/{id}` | Read a report with status history |
| `PATCH` | `/api/reports/{id}/status` | Change status and append a history event |
| `POST` | `/api/analysis/report` | Suggest structured report details without saving a report |

## AI integration

Phase 3 uses the OpenAI Responses API with Structured Outputs. A resident's description and location are transformed into a validated title, category, severity, factual summary, missing-information prompts, and an optional immediate-safety warning. Analysis is advisory and does not create or modify a report.

The API key remains server-side, provider access is isolated behind `ReportAnalysisService`, and the Pydantic response model rejects values outside CivicFix's existing report enums. Provider errors and missing configuration return `503` without exposing internal exception details.

## Testing

Automated backend verification:

```powershell
cd backend
python -m pip install -r requirements-dev.txt
python -m pytest -q
```

Frontend verification:

```powershell
cd frontend
npm run build
```

With the backend running:

```powershell
Invoke-RestMethod http://localhost:8000/api/health
```

Expected status is `ok`. Use `http://localhost:8000/docs` to create a report, list it, retrieve it by UUID, and update its status.

## Zerops deployment

`zerops-import.yaml` drafts the project services: a public frontend, a backend, and a single-node staging PostgreSQL service. `zerops.yaml` drafts separate build/run pipelines and health checks for the two application services.

This is intentionally a draft until Phase 8. The backend draft applies Alembic migrations before starting and receives the managed database connection string from Zerops. Before deployment, validate service-generated variables, public routing, cross-origin configuration, and build artifact paths against the selected project.

## Security considerations

- Configuration is environment-based; secrets must not enter source control.
- CORS permits explicit origins rather than a wildcard.
- FastAPI validates response schemas.
- Future uploads will require type, content, and size validation.
- Production errors must not expose internal tracebacks.

## Known limitations

- The landing page is informational only; report CRUD and AI analysis are API-only.
- There is no image upload, duplicate detection, authentication, or admin dashboard.
- Landing-page statistics describe workflow structure, not fabricated user or report counts.
- Zerops configuration is a Phase 1 draft and has not been deployed.
- PostgreSQL could not be integration-tested locally because Docker/PostgreSQL is not installed in the current environment; CRUD behavior is covered with an isolated SQLite database using the same SQLAlchemy models.
- The current stable Next.js 15 release builds successfully, but npm reports four high-severity production advisories in its bundled `postcss`/`nanoid` and `sharp` dependency chain. No non-breaking stable upgrade is currently offered by npm; re-audit before deployment.

## Future improvements

Work will continue with image upload; duplicate detection; admin dashboard; security and testing; Zerops deployment; and production verification.
