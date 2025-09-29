# Contributing to RainRef

## Dev setup
- `docker compose -f infra/docker-compose.yml up --build`
- API at http://localhost:8080, Web at http://localhost:5173
- `make test` (API) · `make web` (dev) · `make migrate-seed`

## Coding standards
- Python: type hints, ruff + black
- Web: TS strict, eslint + prettier
- Tests: pytest unit/e2e; keep fast and deterministic

## PRs
- Small, focused changes
- Include tests and docs when adding features
