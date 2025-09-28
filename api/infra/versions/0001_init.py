from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0001'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    op.create_table(
        'kb_cards',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('title', sa.Text, nullable=False),
        sa.Column('body', sa.Text, nullable=False),
        sa.Column('tags', postgresql.ARRAY(sa.Text), nullable=False, server_default='{}'),
        sa.Column('embedding', postgresql.ARRAY(sa.Float), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'ref_events',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('source', sa.Text, nullable=False),
        sa.Column('channel', sa.Text, nullable=False),
        sa.Column('product', sa.Text, nullable=True),
        sa.Column('user_ref', sa.Text, nullable=True),
        sa.Column('text', sa.Text, nullable=False),
        sa.Column('context', postgresql.JSONB, nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'tickets',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('ref_event_id', sa.String(length=64), sa.ForeignKey('ref_events.id', ondelete='SET NULL')),
        sa.Column('status', sa.Text, nullable=False, server_default='draft'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'actions',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('ticket_id', sa.String(length=64), sa.ForeignKey('tickets.id', ondelete='CASCADE')),
        sa.Column('type', sa.Text, nullable=False),
        sa.Column('params', postgresql.JSONB, nullable=False, server_default='{}'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'product_signals',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('origin', sa.Text, nullable=False),
        sa.Column('type', sa.Text, nullable=False),
        sa.Column('product_area', sa.Text, nullable=True),
        sa.Column('strength', sa.Float, nullable=False, server_default='0'),
        sa.Column('evidence_refs', postgresql.ARRAY(sa.Text), nullable=False, server_default='{}'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )

    op.create_table(
        'audit_log',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('receipt_id', sa.Text, nullable=False),
        sa.Column('verified', sa.Boolean, nullable=False, server_default='false'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()')),
    )


def downgrade() -> None:
    op.drop_table('audit_log')
    op.drop_table('product_signals')
    op.drop_table('actions')
    op.drop_table('tickets')
    op.drop_table('ref_events')
    op.drop_table('kb_cards')
