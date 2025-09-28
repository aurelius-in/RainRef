from alembic.config import Config
from alembic import command
import os

CFG_PATH = os.path.join(os.path.dirname(__file__), "alembic.ini")

def upgrade_head() -> None:
    cfg = Config(CFG_PATH)
    command.upgrade(cfg, "head")

if __name__ == "__main__":
    upgrade_head()
