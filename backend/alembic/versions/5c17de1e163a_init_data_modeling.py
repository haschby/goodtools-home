"""Init Data Modeling

Revision ID: 5c17de1e163a
Revises: 
Create Date: 2026-07-28 21:34:50.079717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5c17de1e163a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'buyback',
        sa.Column(
            'status',
            sa.Enum('A Traiter', 'Valider', name='statusbuybackenum'),
            nullable=False,
        ),
        sa.Column('gc_booking', sa.String(length=255), nullable=True),
        sa.Column('file_path', sa.Text(), nullable=True),
        sa.Column('amount', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            'id',
            sa.String(length=36),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )
    op.create_index(
        'ix_buybacks_created_at_id', 'buyback', ['created_at', 'id'], unique=False
    )
    op.create_index(
        'ix_buybacks_status_created_at_id',
        'buyback',
        ['status', 'created_at', 'id'],
        unique=False,
    )
    
    op.create_unique_constraint(None, 'invoice', ['id'])
    op.create_unique_constraint(None, 'user', ['id'])
    op.create_unique_constraint(None, 'workflow', ['id'])
    op.create_unique_constraint(None, 'workflow_step', ['id'])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, 'workflow_step', type_='unique')
    op.drop_constraint(None, 'workflow', type_='unique')
    op.drop_constraint(None, 'user', type_='unique')
    op.drop_constraint(None, 'invoice', type_='unique')
    op.drop_index('ix_buybacks_status_created_at_id', table_name='buyback')
    op.drop_index('ix_buybacks_created_at_id', table_name='buyback')
    op.drop_table('buyback')
    sa.Enum(name='statusbuybackenum').drop(op.get_bind(), checkfirst=True)
