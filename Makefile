
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
