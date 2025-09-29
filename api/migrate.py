from alembic.config import Config
from alembic import command
import os


def make_config() -> Config:
    # Build config in code to avoid BOM/encoding issues reading ini
    cfg = Config()
    cfg.set_main_option("script_location", "infra")
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:postgres@db:5432/rainref")
    cfg.set_main_option("sqlalchemy.url", db_url)
    return cfg


def upgrade_head() -> None:
    cfg = make_config()
    command.upgrade(cfg, "head")


if __name__ == "__main__":
    upgrade_head()
