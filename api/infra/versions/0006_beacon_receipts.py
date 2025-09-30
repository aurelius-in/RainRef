from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'beacon_receipts',
        sa.Column('id', sa.String(length=64), primary_key=True),
        sa.Column('signature', sa.Text(), nullable=False),
        sa.Column('timestamp', sa.Integer(), nullable=False),
        sa.Column('payload', postgresql.JSONB(astext_type=sa.Text()), nullable=False, server_default=sa.text("'{}'::jsonb")),
    )
    op.create_index('ix_beacon_receipts_ts', 'beacon_receipts', ['timestamp'], unique=False)


def downgrade() -> None:
    op.drop_index('ix_beacon_receipts_ts', table_name='beacon_receipts')
    op.drop_table('beacon_receipts')


