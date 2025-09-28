from alembic import op
import sqlalchemy as sa

revision = '0002'
down_revision = '0001'
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_index('ix_ref_events_source', 'ref_events', ['source'], unique=False)
    op.create_index('ix_ref_events_channel', 'ref_events', ['channel'], unique=False)
    op.create_index('ix_tickets_status', 'tickets', ['status'], unique=False)
    op.create_index('ix_actions_type', 'actions', ['type'], unique=False)
    op.create_index('ix_product_signals_type', 'product_signals', ['type'], unique=False)
    op.create_index('ix_audit_log_receipt_id', 'audit_log', ['receipt_id'], unique=False)
    # GIN index on kb_cards.tags if extension is present
    op.execute("CREATE INDEX IF NOT EXISTS ix_kb_cards_tags ON kb_cards USING GIN (tags);")


def downgrade() -> None:
    op.drop_index('ix_audit_log_receipt_id', table_name='audit_log')
    op.drop_index('ix_product_signals_type', table_name='product_signals')
    op.drop_index('ix_actions_type', table_name='actions')
    op.drop_index('ix_tickets_status', table_name='tickets')
    op.drop_index('ix_ref_events_channel', table_name='ref_events')
    op.drop_index('ix_ref_events_source', table_name='ref_events')
    op.execute("DROP INDEX IF EXISTS ix_kb_cards_tags;")
