# CivicFix Backend MVP

CivicFix is a civic issue reporting API built for the Zerops Developer Challenge. Residents can submit local maintenance problems—such as potholes, broken streetlights, garbage, water leaks, and damaged infrastructure—and track each report through resolution.

## Problem it solves

Community maintenance problems are often reported through disconnected channels with incomplete information and no consistent status trail. CivicFix establishes one validated report format and a predictable status workflow that future resident and operator interfaces can share.

## Current status

The backend MVP is complete and ready for deployment testing on Zerops:

- FastAPI REST API with Swagger/OpenAPI documentation
- PostgreSQL persistence through SQLAlchemy and Psycopg 3
- Alembic database migrations
- Report creation, listing, retrieval, and status updates
- Environment-based database and CORS configuration
- Python 3.12 Zerops pipeline for the existing `api` service
- Automated endpoint tests

Frontend development, authentication, uploads, AI, Redis, and background workers are intentionally outside the current scope.

## Technology stack

- Python 3.12
- FastAPI and Uvicorn
- PostgreSQL 18
- SQLAlchemy 2 and Psycopg 3
- Pydantic Settings
- Alembic
- Pytest

## Project structure

```text
backend/
├── alembic/               # Database migration environment and revisions
├── app/
│   ├── api/               # FastAPI route handlers
│   ├── models/            # SQLAlchemy persistence models
│   ├── repositories/      # Database access
│   ├── schemas/           # Pydantic request and response models
│   ├── services/          # Business rules and HTTP errors
│   ├── config.py          # Environment-based settings
│   ├── database.py        # Engine, sessions, and declarative base
│   └── main.py            # FastAPI application and CORS
├── tests/                 # API tests
├── alembic.ini
├── requirements.txt
└── start.py               # PORT-aware production entry point
```

## API endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Return API health status |
| `POST` | `/api/reports` | Create a report |
| `GET` | `/api/reports` | List all reports |
| `GET` | `/api/reports/{id}` | Retrieve one report |
| `PATCH` | `/api/reports/{id}/status` | Update report status |

Swagger UI is available at `/docs`, ReDoc at `/redoc`, and the generated schema at `/openapi.json`.

`GET /api/reports` accepts optional `category`, `severity`, and `status` query parameters. Values are validated against the enums below and can be combined.

### Report values

Categories:

`ROAD`, `STREETLIGHT`, `GARBAGE`, `WATER`, `INFRASTRUCTURE`, `OTHER`

Severity levels:

`LOW`, `MEDIUM`, `HIGH`, `CRITICAL`

Statuses:

`REPORTED`, `UNDER_REVIEW`, `ASSIGNED`, `IN_PROGRESS`, `RESOLVED`

### Create a report

```http
POST /api/reports
Content-Type: application/json
```

```json
{
  "title": "Large pothole near junction",
  "description": "A deep pothole is forcing vehicles into the opposite lane.",
  "category": "ROAD",
  "severity": "HIGH",
  "latitude": 28.6139,
  "longitude": 77.209
}
```

New reports receive the `REPORTED` status automatically.

`latitude` and `longitude` are optional. When provided, latitude must be between -90 and 90 and longitude between -180 and 180.

### Update report status

```json
{
  "status": "UNDER_REVIEW"
}
```

## Local development

Requirements:

- Python 3.12
- Docker Desktop with Docker Compose

Start PostgreSQL from the repository root:

```powershell
docker compose up -d db
docker compose ps
```

Create the backend environment and install dependencies:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
Copy-Item .env.example .env
```

Apply database migrations:

```powershell
python -m alembic upgrade head
```

Start the development API:

```powershell
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/docs`.

## Tests

From `backend/` with the virtual environment activated:

```powershell
python -m pytest -q
```

The current suite covers health checks, report creation, report listing, individual report retrieval, status updates, input validation, missing reports, and resolved-report protection.

Tests use an isolated in-memory SQLite database through FastAPI's database dependency override. This keeps endpoint tests deterministic and does not replace PostgreSQL in the application or deployment. PostgreSQL migration and persistence behavior should also be verified locally before deployment.

## Environment variables

| Variable | Purpose | Local example/default |
| --- | --- | --- |
| `DATABASE_URL` | Required SQLAlchemy database connection | `postgresql+psycopg://civicfix:civicfix@localhost:5432/civicfix` |
| `CORS_ORIGINS` | Comma-separated allowed browser origins | `http://localhost:3000` |
| `ENVIRONMENT` | Runtime environment label | `development` |
| `PORT` | HTTP port used by `backend/start.py` | `8000` |

Never commit real credentials or a populated `.env` file.

## Zerops deployment

The root `zerops.yaml` targets the services already created in the `civicfix` project:

- `api`: Python 3.12 runtime
- `db`: PostgreSQL 18.1

The `api` setup:

- installs backend dependencies during the build
- receives `DATABASE_URL` from `${db_connectionString}`
- applies Alembic migrations before starting
- listens on `0.0.0.0` and uses `PORT`, defaulting to `8000`
- exposes port 8000 with HTTP support
- checks `/api/health`

Deployment remains a manual step: connect the public GitHub repository to the existing Zerops `api` service when ready.

## Current limitations

- There is no frontend or resident-facing submission form.
- There is no authentication or authorization.
- Reports cannot include images or attachments.
- Status changes are not stored as a separate audit history.
- The list endpoint does not yet paginate.
- Tests cover API behavior with SQLite; a PostgreSQL integration test environment is still recommended.

## Planned AI functionality

AI is not implemented in Phase 1. A later phase may use a server-side provider integration to suggest a report title, category, severity, and missing details from natural-language descriptions and optional images. Provider credentials will remain in environment variables, outputs will be validated before use, and residents will review suggestions before submitting a report.
