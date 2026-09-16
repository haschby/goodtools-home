"""add index on invoice.gc_booking

Revision ID: f2c3d4e5a6b7
Revises: e7f1a2b3c4d5
Create Date: 2026-09-16 09:57:00.000000

Speeds up ``InvoiceRepositoryImpl.get_by_external_ids`` which filters invoices
by ``id`` / ``external_id`` / ``gc_booking``. The first two columns are already
indexed (primary key + unique index) but ``gc_booking`` was not, forcing a
sequential scan of the whole ``invoice`` table on every rentability lookup.

The index is created ``CONCURRENTLY`` so it does not lock the table in
production; that requires running outside of a transaction block.
"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'f2c3d4e5a6b7'
down_revision: Union[str, Sequence[str], None] = 'e7f1a2b3c4d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # CONCURRENTLY cannot run inside a transaction, so drive the connection in
    # autocommit mode for the duration of the index creation.
    with op.get_context().autocommit_block():
        op.execute(
            'CREATE INDEX CONCURRENTLY IF NOT EXISTS '
            'ix_invoice_gc_booking ON invoice ("gc_booking")'
        )


def downgrade() -> None:
    with op.get_context().autocommit_block():
        op.execute(
            'DROP INDEX CONCURRENTLY IF EXISTS ix_invoice_gc_booking'
        )
