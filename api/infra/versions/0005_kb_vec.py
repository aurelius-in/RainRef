from alembic import op
import sqlalchemy as sa


revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Ensure pgvector extension
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    # Add vector column if missing
    op.execute(
        """
        DO $$
        BEGIN
          IF NOT EXISTS (
            SELECT 1 FROM information_schema.columns
            WHERE table_name='kb_cards' AND column_name='embedding_vec'
          ) THEN
            ALTER TABLE kb_cards ADD COLUMN embedding_vec vector(1536);
          END IF;
        END$$;
        """
    )
    # Create IVFFlat index for vector similarity (requires ANALYZE for performance)
    op.execute(
        """
        DO $$
        BEGIN
          IF to_regclass('public.ix_kb_cards_vec') IS NULL THEN
            CREATE INDEX ix_kb_cards_vec ON kb_cards USING ivfflat (embedding_vec vector_l2_ops) WITH (lists = 100);
          END IF;
        END$$;
        """
    )
    # Optional backfill from existing numeric array if present; ignore on failure
    op.execute(
        """
        DO $$
        BEGIN
          BEGIN
            UPDATE kb_cards SET embedding_vec = embedding WHERE embedding_vec IS NULL AND embedding IS NOT NULL;
          EXCEPTION WHEN others THEN
            -- Ignore casting errors in dev; new cards will have embeddings
            NULL;
          END;
        END$$;
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_kb_cards_vec;")


