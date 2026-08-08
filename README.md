# LogPulse

LogPulse is a lightweight log ingestion and authentication platform targeted for local development and experimentation. It is organized as small containerized services that demonstrate an auth API, an asynchronous log processor (Celery), and a React frontend.

Key components:

- Auth Service — FastAPI-based API for user management and authentication.
- Processor Service — FastAPI + Celery workers for asynchronous log processing.
- PostgreSQL — persistent store for auth data.
- Redis — Celery broker and result backend.
- Frontend — Vite + React UI (Tailwind CSS used in the project).

Repository layout

- `logpulse_backend/scripts/services/auth-service/` — authentication API, DB models, tests.
- `logpulse_backend/scripts/services/processor-service/` — processor API, Celery tasks, worker config.
- `frontend/` — React app (Vite).
- `docker-compose.yml` — local composition of services for development.
- `logpulse_backend/scripts/run-local.sh` — helper script that runs `docker-compose up --build`.
- `.env.example` — environment variable examples used by the services.

Quick start (recommended)

1. Copy the example env file and edit required values:

```bash
cp .env.example .env
# Edit .env and set realistic values. Example:
# AUTH_DATABASE_URL=postgresql://auth_user:password@postgres:5432/auth_db
# PROCESSOR_BROKER_URL=redis://redis:6379/0
# PROCESSOR_RESULT_BACKEND=redis://redis:6379/1
```

Note: `.env.example` contains placeholder/masked DB URLs; replace them with correct values before starting.

2. Start the full local stack (requires Docker & Docker Compose):

```bash
./logpulse_backend/scripts/run-local.sh
# or
docker-compose up --build
```

3. After services are healthy, open:

- Auth API (FastAPI): http://localhost:8000
- Processor API (if exposed): http://localhost:8001
- Frontend: run the frontend dev server (see below) or use a built build.

Frontend development

To run the frontend dev server (recommended while developing UI):

```bash
cd frontend
npm install
npm run dev
# dev server typically runs on http://localhost:5173 (check output)
```

To build a production bundle:

```bash
cd frontend
npm install
npm run build
npm run preview
```

Running services without Docker (local Python development)

1. Create and activate a virtual environment and install deps for the service:

```bash
python -m venv .venv
source .venv/bin/activate
cd logpulse_backend/scripts/services/auth-service
pip install -r requirements.txt
```

2. Set the same environment variables from `.env` (or export them) and run:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Processor/Celery worker (local)

When running locally (without Docker), install the processor requirements and start a worker using the same app entrypoint used in compose:

```bash
cd logpulse_backend/scripts/services/processor-service
pip install -r requirements.txt
# start api
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
# in another terminal start worker (example used in compose):
celery -A app.core.celery_app.celery_app worker -I app.tasks --loglevel=info
```

Environment variables (summary)

- AUTH_DATABASE_URL — full SQLAlchemy/Postgres URL for the auth DB (example: postgresql://auth_user:password@postgres:5432/auth_db)
- AUTH_JWT_SECRET — secret used to sign JWTs
- AUTH_ACCESS_TOKEN_EXPIRE_MINUTES — token TTL in minutes
- PROCESSOR_BROKER_URL — Redis broker (e.g. redis://redis:6379/0)
- PROCESSOR_RESULT_BACKEND — Redis result backend (e.g. redis://redis:6379/1)
- LOG_LEVEL — logging level (info, debug, etc.)

Docker Compose notes

- Services defined in `docker-compose.yml` include `postgres` (5432), `redis` (6379), `auth-service` (8000), `processor-service` (8001) and a `celery-worker` service.
- If host ports 5432 or 6379 are already used on your machine, update `docker-compose.yml` or stop the conflicting services.

Running tests

Each service contains tests runnable with pytest. Example:

```bash
cd logpulse_backend/scripts/services/auth-service
pytest
```

```bash
cd logpulse_backend/scripts/services/processor-service
pytest
```

Troubleshooting

- If the services fail to start, check docker-compose logs:

```bash
docker-compose logs -f
```

- Ensure `.env` contains valid DB/Redis URLs. The example file uses masked placeholders that must be replaced.

Further documentation

- See [LOGPULSE_STRUCTURE.md](/home/gayantha/LogPulse/LOGPULSE_STRUCTURE.md) for an overview of the code layout.
- See [INFRASTRUCTURE.md](/home/gayantha/LogPulse/INFRASTRUCTURE.md) for deployment/infrastructure notes.

Contributing & Issues

Please open issues on the repository for bugs, feature requests or setup problems.

License

This project is available under the terms of the LICENSE file in the repository.
