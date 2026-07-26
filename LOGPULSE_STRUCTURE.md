# LogPulse Project Structure

## Frontend

- `frontend/`
  - `package.json`
  - `postcss.config.js`
  - `tailwind.config.js`
  - `src/`
    - `main.jsx`
    - `App.jsx`
    - `index.css`
    - `components/LogPulseDashboard.jsx`

## Backend

- `logpulse_backend/`
  - `scripts/`
    - `init-db.sh`
    - `run-local.sh`
    - `services/`
      - `auth-service/`
        - `.dockerignore`
        - `Dockerfile`
        - `requirements.txt`
        - `app/`
          - `main.py`
          - `api/`
            - `v1/`
              - `router.py`
              - `endpoints/auth.py`
          - `core/`
            - `config.py`
            - `database.py`
            - `security.py`
          - `models/user.py`
          - `schemas/user.py`
          - `services/user_service.py`
        - `tests/`
          - `conftest.py`
          - `test_auth.py`
      - `processor-service/`
        - `Dockerfile`
        - `pytest.ini`
        - `requirements.txt`
        - `app/`
          - `main.py`
          - `core/`
            - `celery_app.py`
            - `config.py`
          - `schemas/log_entry.py`
          - `tasks/log_tasks.py`
        - `tests/`
          - `conftest.py`
          - `test_healthz.py`

## Infrastructure

- `docker-compose.yml`
- `docker-compose.override.yml`
- `k8s/`
  - `auth-service/`
    - `configmap.yml`
  - `base/`
    - `ingress.yml`
    - `postgres/`
      - `deployment.yml`
      - `pvc.yml`
      - `service.yml`
    - `redis/`
      - `deployment.yml`
      - `service.yml`
  - `processor-service/`
    - `deployment.yml`
    - `service.yml`
- `helm/analytics-platform/`
  - `Chart.yaml`
  - `values.yaml`

## Root Files

- `README.md`
- `.env.example`
- `LICENSE`
- `LOGPULSE_STRUCTURE.md`
- `.github/workflows/`
  - `auth-service-ci.yml`
  - `processor-service-ci.yml`
  - `k8s-deploy.yml`
