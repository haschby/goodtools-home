"""add_invoice_type_column

Revision ID: bb82b0c2c632
Revises: c9faa38b87e5
Create Date: 2026-09-03 09:57:08.742271

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb82b0c2c632'
down_revision: Union[str, Sequence[str], None] = 'c9faa38b87e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


enum_invoice_type = sa.Enum('provider', 'buyback', name='enuminvoicetype')


def upgrade() -> None:
    """Upgrade schema."""
    # Drop any pre-existing column/type so we always end up with the
    # lowercase labels ('provider', 'buyback'), even if an older version of
    # this enum (e.g. FACTURE/BOOKING/RACHAT) already exists in the database.
    op.execute("ALTER TABLE invoice DROP COLUMN IF EXISTS invoice_type")
    op.execute("DROP TYPE IF EXISTS enuminvoicetype")

    enum_invoice_type.create(op.get_bind(), checkfirst=True)
    op.add_column(
        'invoice',
        sa.Column(
            'invoice_type',
            sa.Enum('provider', 'buyback', name='enuminvoicetype', create_type=False),
            nullable=True,
            server_default='provider',
        )
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('invoice', 'invoice_type')
    op.execute("DROP TYPE IF EXISTS enuminvoicetype")
