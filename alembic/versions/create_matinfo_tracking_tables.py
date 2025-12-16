"""Create Matinfo GTIN tracking tables

Revision ID: create_matinfo_tracking
Revises:
Create Date: 2025-09-29

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text


# revision identifiers, used by Alembic.
revision = 'create_matinfo_tracking'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create new tables for tracking Matinfo GTIN updates."""

    # Create matinfo_gtin_updates table
    op.create_table('matinfo_gtin_updates',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('gtin', sa.String(length=20), nullable=False),
        sa.Column('update_date', sa.DateTime(), nullable=False, comment='Date when GTIN was updated in Matinfo'),
        sa.Column('sync_date', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), comment='Date when we fetched this update'),
        sa.Column('synced', sa.Boolean(), default=False, comment='Whether product data has been synced'),
        sa.Column('sync_status', sa.String(length=50), comment='Status of sync: pending, success, failed, skipped'),
        sa.Column('error_message', sa.Text(), nullable=True, comment='Error message if sync failed'),
        sa.Column('product_name', sa.String(length=255), nullable=True, comment='Product name if available'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.Column('updated_at', sa.DateTime(), onupdate=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_matinfo_gtin', 'matinfo_gtin_updates', ['gtin'], unique=False)
    op.create_index('idx_matinfo_sync_status', 'matinfo_gtin_updates', ['sync_status'], unique=False)

    # Create matinfo_sync_logs table
    op.create_table('matinfo_sync_logs',
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('sync_type', sa.String(length=50), comment='Type of sync: full, incremental, single'),
        sa.Column('start_date', sa.DateTime(), nullable=False, comment='Start date of sync operation'),
        sa.Column('end_date', sa.DateTime(), nullable=True, comment='End date of sync operation'),
        sa.Column('since_date', sa.DateTime(), nullable=True, comment='Date from which updates were fetched'),
        sa.Column('total_gtins', sa.Integer(), default=0, comment='Total number of GTINs to process'),
        sa.Column('synced_count', sa.Integer(), default=0, comment='Number of successfully synced products'),
        sa.Column('failed_count', sa.Integer(), default=0, comment='Number of failed syncs'),
        sa.Column('status', sa.String(length=50), comment='Status: running, completed, failed'),
        sa.Column('error_message', sa.Text(), nullable=True, comment='Error message if sync failed'),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP')),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_sync_log_status', 'matinfo_sync_logs', ['status'], unique=False)
    op.create_index('idx_sync_log_created', 'matinfo_sync_logs', ['created_at'], unique=False)


def downgrade():
    """Drop Matinfo tracking tables."""
    op.drop_index('idx_sync_log_created', table_name='matinfo_sync_logs')
    op.drop_index('idx_sync_log_status', table_name='matinfo_sync_logs')
    op.drop_table('matinfo_sync_logs')

    op.drop_index('idx_matinfo_sync_status', table_name='matinfo_gtin_updates')
    op.drop_index('idx_matinfo_gtin', table_name='matinfo_gtin_updates')
    op.drop_table('matinfo_gtin_updates')