# RainRef Deployment Guide

This document summarizes recommended production deployment steps and settings.

## Components
- API (FastAPI)
- Web (Vite/React, static hosting ok)
- Postgres with pgvector
- OPA (Open Policy Agent)
- Optional: Redis for global rate limiting
- Optional: Azurite (use real Azure Blob in prod), OTEL collector

## Environment Variables (API)
- DATABASE_URL: postgresql+psycopg://USER:PASS@HOST:5432/DB
- ALLOWED_ORIGINS: ["https://app.example.com"]
- API_KEY: optional admin key for bootstrap
- JWT_SECRET: required for JWT auth
- REQUIRE_JWT_FOR_ADMIN: true
- OPA_URL: http://opa:8181
- ENABLE_HSTS: true
- ZENDESK_BASE_URL / ZENDESK_TOKEN
- INTERCOM_BASE_URL / INTERCOM_TOKEN
- GITHUB_REPO / GITHUB_TOKEN
- RAINBEACON_SECRET: HMAC key for receipts
- OTEL_EXPORTER_OTLP_ENDPOINT: optional
- USE_REDIS_LIMITER: true|false
- REDIS_URL: redis://redis:6379/0

## Docker Compose (prod)
Use `infra/docker-compose.prod.yml` as a starting point. Example:

```bash
docker compose -f infra/docker-compose.prod.yml --env-file .env.prod up -d --build
```

After boot:
```bash
docker compose -f infra/docker-compose.prod.yml exec api python api/migrate.py
docker compose -f infra/docker-compose.prod.yml exec api python api/seed.py
```

## Security Headers
The API sets strong defaults:
- HSTS (enable via ENABLE_HSTS=true)
- X-Content-Type-Options, X-Frame-Options, Referrer-Policy
- COOP/COEP/CORP
- CSP (adjust connect-src for your domains)

## Rate Limiting
Global limiter supports:
- In-memory per-IP (default)
- Redis-backed per-IP (set USE_REDIS_LIMITER=true and REDIS_URL)
Configure windows via:
- rate_limit_window_sec (default 60)
- rate_limit_per_window (default 100)

Tune via environment in `api/config.py`.

## Data and Backups
- Enable regular Postgres backups
- Consider separate volume for `db_data`
- Monitor DB with pg_stat_statements

## Observability
- Set OTEL exporter env vars
- Consider external tracing (Jaeger, Tempo) and logs

## CI/CD
- GitHub Actions runs unit tests and docker E2E + Playwright
- Protect branches and require CI checks before deploy

## Hardening Checklist
- Set real secrets and rotate on schedule
- Restrict CORS origins
- Configure adapters via /admin or env
- Enforce JWT for admin (`REQUIRE_JWT_FOR_ADMIN=true`)
- Review OPA policies for all action types
- Review CSP for frontend hosting location

## Scaling
- Run multiple API replicas behind a reverse proxy (nginx/traefik)
- Use sticky sessions if adding in-memory limits (or move to Redis)
- Add a real rate limiter (e.g., Redis-based) for multi-instance
