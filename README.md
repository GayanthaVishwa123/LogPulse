# LogPulse

LogPulse is a lightweight log processing and authentication platform designed for local development with Docker Compose. It provides:

- **Auth Service**: a FastAPI service handling authentication and user management.
- **Processor Service**: a FastAPI + Celery service for processing logs asynchronously.
- **PostgreSQL**: persistent auth database storage.
- **Redis**: Celery broker and result backend.
- **Frontend**: Vite + React UI using Tailwind CSS.

## Repository Structure

- `logpulse_backend/scripts/services/auth-service/`: authentication API, database, and user models.
- `logpulse_backend/scripts/services/processor-service/`: log processor, Celery tasks, and worker config.
- `frontend/`: React frontend app.
- `docker-compose.yml`: local service orchestration.
- `logpulse_backend/scripts/run-local.sh`: helper script to launch the local environment.
- `.env.example`: example environment variables for both services.

## Architecture

LogPulse is organized as a small containerized microservice platform:

- **Frontend**: Vite + React UI in `frontend/`.
- **Auth Service**: FastAPI service in `logpulse_backend/scripts/services/auth-service/` using PostgreSQL for user/auth data.
- **Processor Service**: FastAPI + Celery service in `logpulse_backend/scripts/services/processor-service/` using Redis for task queuing and results.
- **Infrastructure**: `docker-compose.yml` for local stacks, `k8s/` manifests for Kubernetes base services, and `helm/` for deployment packaging.

The services communicate via standard HTTP APIs and share infrastructure resources like PostgreSQL and Redis.

## Prerequisites

- Docker
- Docker Compose
- Git

## Local Development

1. Copy environment variables:

```bash
cp .env.example .env
```

2. Start the stack:

```bash
./logpulse_backend/scripts/run-local.sh
```

3. Open the services:

- Auth service: `http://localhost:8000`
- Frontend: configure via `frontend` dev server if enabled separately

## Services

### Auth Service

- Build context: `logpulse_backend/scripts/services/auth-service`
- Ports: `8000:8000`
- Database: `postgres`
- Main frameworks: FastAPI, SQLAlchemy, asyncpg, PyJWT

### Processor Service

- Build context: `logpulse_backend/scripts/services/processor-service`
- Depends on: `redis`
- Worker backend: Celery with Redis broker and result backend

## Environment Variables

The project uses `.env.example` for configuration:

- `AUTH_DATABASE_URL`: PostgreSQL database URL for auth service
- `AUTH_JWT_SECRET`: JWT signing secret
- `AUTH_ACCESS_TOKEN_EXPIRE_MINUTES`: token expiration
- `PROCESSOR_BROKER_URL`: Redis broker URL for Celery
- `PROCESSOR_RESULT_BACKEND`: Redis backend URL for Celery results
- `LOG_LEVEL`: application log level

## Docker Compose

The local compose stack includes:

- `postgres`: Postgres 15 for auth storage
- `redis`: Redis 7 for Celery broker
- `auth-service`: app service for authentication
- `processor-service`: Celery processor service

## Running Tests

Each service includes its own tests. Run them from the service folder, for example:

```bash
cd logpulse_backend/scripts/services/auth-service
pytest
```

```bash
cd logpulse_backend/scripts/services/processor-service
pytest
```

## Useful Commands

- Build frontend:

```bash
cd frontend
npm install
npm run build
```

- Run backend auth service locally (without Docker):

```bash
cd logpulse_backend/scripts/services/auth-service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- Run processor service locally:

```bash
cd logpulse_backend/scripts/services/processor-service
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001
```

## Notes

- The frontend currently uses Vite and React; its dev server can be launched from `frontend/`.
- Ensure `.env` is present and updated before starting the services.
