from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add tsv column and trigger for kb_cards if missing
    op.execute(
        """
        DO $$
        BEGIN
          IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name='kb_cards' AND column_name='tsv'
          ) THEN
            ALTER TABLE kb_cards ADD COLUMN tsv tsvector;
            CREATE INDEX IF NOT EXISTS ix_kb_cards_tsv ON kb_cards USING GIN (tsv);
            CREATE TRIGGER tsv_kb_cards_update
            BEFORE INSERT OR UPDATE ON kb_cards
            FOR EACH ROW EXECUTE FUNCTION tsvector_update_trigger(tsv, 'pg_catalog.english', title, body);
            UPDATE kb_cards SET tsv = to_tsvector('english', coalesce(title,'') || ' ' || coalesce(body,'')) WHERE tsv IS NULL;
          END IF;
        END$$;
        """
    )


def downgrade() -> None:
    op.execute("DROP TRIGGER IF EXISTS tsv_kb_cards_update ON kb_cards;")
    op.execute("DROP INDEX IF EXISTS ix_kb_cards_tsv;")
    op.execute("ALTER TABLE kb_cards DROP COLUMN IF EXISTS tsv;")


