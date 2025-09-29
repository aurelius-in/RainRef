
migrate:
	cd api && alembic -c alembic.ini upgrade head

revision:
	cd api && alembic -c alembic.ini revision -m "update"

migrate-seed:
	$(MAKE) migrate
	python infra/migrations/seed.py

format:
	cd api && black . && ruff check . --fix
	cd web && npx prettier --write "src/**/*.{ts,tsx}" "index.html"

format-web:
	cd web && npx prettier --write "src/**/*.{ts,tsx}" "index.html" && npx eslint src --ext .ts,.tsx --fix

typecheck-web:
	cd web && npm run typecheck

test-all:
	cd api && pytest -q
	cd web && npm run lint && npm run typecheck
