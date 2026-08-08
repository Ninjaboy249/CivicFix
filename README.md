# CivicFix Backend MVP

CivicFix is a civic issue reporting API for the Zerops Developer Challenge. The current scope is backend-only: residents can submit community maintenance reports and track their status through a PostgreSQL-backed REST API.

Frontend development, authentication, uploads, AI, workers, and Redis are intentionally out of scope for this phase.

## Stack

- Python 3.12
- FastAPI and Uvicorn
- PostgreSQL, SQLAlchemy, and Psycopg 3
- Pydantic Settings
- Alembic
- Pytest

## API

| Method | Path | Purpose |
| --- | --- | --- |
| `GET` | `/api/health` | Service health check |
| `POST` | `/api/reports` | Create a civic report |
| `GET` | `/api/reports` | List reports |
| `GET` | `/api/reports/{id}` | Retrieve one report |
| `PATCH` | `/api/reports/{id}/status` | Update report status |

Interactive API documentation is available at `/docs`; the generated OpenAPI schema is available at `/openapi.json`.

## Local setup

From the repository root:

```powershell
docker compose up -d db
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt -r requirements-dev.txt
Copy-Item .env.example .env
python -m alembic upgrade head
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run tests from `backend/`:

```powershell
python -m pytest -q
```

## Configuration

The backend reads configuration from environment variables or `backend/.env`:

- `DATABASE_URL`: SQLAlchemy database URL. Zerops can supply `${db_connectionString}`.
- `CORS_ORIGINS`: comma-separated list of allowed frontend origins.
- `ENVIRONMENT`: runtime environment name.
- `PORT`: runtime HTTP port, defaulting to `8000` in `backend/start.py`.

Do not commit real credentials or a populated `.env` file.

## Zerops

The root `zerops.yaml` targets the existing `api` Python 3.12 service, installs backend dependencies, applies migrations during startup, exposes HTTP port 8000, and checks `/api/health`. It receives the PostgreSQL connection string from the existing `db` service.
