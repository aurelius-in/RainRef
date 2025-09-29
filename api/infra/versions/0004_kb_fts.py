from alembic import op
import sqlalchemy as sa


revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create a GIN index for full-text search over title+body
    op.execute("""
    CREATE INDEX IF NOT EXISTS ix_kb_cards_fts
    ON kb_cards USING GIN (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,'')));
    """)


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_kb_cards_fts;")


