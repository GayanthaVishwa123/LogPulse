# LogPulse Infrastructure

This repository uses Docker Compose for local development and Kubernetes/Helm for cluster deployment.

## Local Development

### Docker Compose

The local stack is defined in `docker-compose.yml` and includes:

- `postgres`: PostgreSQL 15 for authentication storage.
- `redis`: Redis 7 for Celery broker and task results.
- `auth-service`: FastAPI auth microservice.
- `processor-service`: FastAPI + Celery log processor microservice.

A helper script is available at:

- `logpulse_backend/scripts/run-local.sh`

### Environment Variables

Configuration is provided in `.env.example` and should be copied to `.env` before starting the stack.

Key values:

- `AUTH_DATABASE_URL`
- `AUTH_JWT_SECRET`
- `AUTH_ACCESS_TOKEN_EXPIRE_MINUTES`
- `PROCESSOR_BROKER_URL`
- `PROCESSOR_RESULT_BACKEND`
- `LOG_LEVEL`

## Kubernetes

The `k8s/` directory contains manifests for deploying the app on Kubernetes.

### Base Infrastructure

- `k8s/base/ingress.yml` - Ingress routing for auth and processor services.
- `k8s/base/postgres/` - PostgreSQL deployment, PVC, and service.
- `k8s/base/redis/` - Redis deployment and service.

### Service Manifests

- `k8s/auth-service/` - ConfigMap and deployment/service resources for the auth service.
- `k8s/processor-service/` - Deployment, Celery worker deployment, and service resources for the processor service.

## Helm

The Helm chart lives in `helm/analytics-platform/` and provides a packaged deployment for the platform.

### Chart Files

- `helm/analytics-platform/Chart.yaml` - Chart metadata.
- `helm/analytics-platform/values.yaml` - Default values for auth service, processor service, Postgres, and Redis.

### Chart Values

The chart configures:

- `authService`
- `processorService`
- `postgres`
- `redis`

### Recommended Usage

For local Kubernetes testing, install the chart using a tool like `minikube`, `kind`, or a managed cluster:

```bash
helm install logpulse ./helm/analytics-platform
```

To customize the installation, override chart values:

```bash
helm install logpulse ./helm/analytics-platform -f custom-values.yaml
```

## Notes

- The backend microservices are grouped under `logpulse_backend/scripts/services/`.
- The frontend is isolated in `frontend/`.
- `README.md` contains project startup guidance; this file focuses on infrastructure and deployment.
