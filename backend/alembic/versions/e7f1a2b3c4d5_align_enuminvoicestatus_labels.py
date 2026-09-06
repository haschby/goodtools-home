"""align enuminvoicestatus labels with enum values

Revision ID: e7f1a2b3c4d5
Revises: 43d8546efea5
Create Date: 2026-09-04 15:20:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'e7f1a2b3c4d5'
down_revision: Union[str, Sequence[str], None] = '43d8546efea5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename enum labels from member names to their business values.

    The invoice status column is persisted using the enum *value*
    (e.g. "A Traiter") instead of the member name (e.g. "TO_BE_TRAITED"),
    because ``EnumInvoiceStatus`` is mapped with ``use_values=True``.

    The Postgres type ``enuminvoicestatus`` was originally created with the
    member names, which no longer match what the ORM writes. Renaming the
    labels in place preserves existing rows. ``VALIDATED_ONLY`` ("Payé") was
    never present in the type, so it is added.
    """
    # Rename existing labels (member name -> business value).
    # "TBD" already matches its value and is intentionally left untouched.
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'ALL' TO 'All'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'ARCHIVED' TO 'Archivé'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'TO_BE_TRAITED' TO 'A Traiter'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'NEED_TO_CHECK' TO 'Avoiriser'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'TO_BE_INVOICED' TO 'A Facturer'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'INVOICED' TO 'Facturer ticket'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'VALIDATED' TO 'A Payer'")

    # Add the label that was missing from the type entirely.
    op.execute("ALTER TYPE enuminvoicestatus ADD VALUE IF NOT EXISTS 'Payé'")


def downgrade() -> None:
    """Revert enum labels back to the member names.

    Note: the added 'Payé' label cannot be dropped (Postgres has no
    ``ALTER TYPE ... DROP VALUE``), so it is left in place on downgrade.
    """
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'All' TO 'ALL'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'Archivé' TO 'ARCHIVED'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'A Traiter' TO 'TO_BE_TRAITED'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'Avoiriser' TO 'NEED_TO_CHECK'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'A Facturer' TO 'TO_BE_INVOICED'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'Facturer ticket' TO 'INVOICED'")
    op.execute("ALTER TYPE enuminvoicestatus RENAME VALUE 'A Payer' TO 'VALIDATED'")
