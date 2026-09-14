"""align enuminvoicestatus labels with enum values

Revision ID: e7f1a2b3c4d5
Revises: 43d8546efea5
Create Date: 2026-09-04 15:20:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e7f1a2b3c4d5'
down_revision: Union[str, Sequence[str], None] = '43d8546efea5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Business values persisted by the ORM (EnumInvoiceStatus, use_values=True).
INVOICE_STATUS_VALUES = (
    'All',
    'TBD',
    'Archivé',
    'A Traiter',
    'Avoiriser',
    'A Facturer',
    'Facturer ticket',
    'A Payer',
    'Payé',
)

enum_invoice_status = sa.Enum(*INVOICE_STATUS_VALUES, name='enuminvoicestatus')


def upgrade() -> None:
    """Create the ``enuminvoicestatus`` type and convert ``invoice.status``.

    Historically ``invoice.status`` was created as a plain ``VARCHAR`` (see the
    init migration), while the ORM maps it as an enum column using the business
    *values* (``EnumInvoiceStatus`` with ``use_values=True``). This migration
    reconciles the database with the ORM by creating the Postgres enum type and
    converting the column to it, mapping any legacy label to its final value.
    """
    bind = op.get_bind()

    # Create the enum type with the final business labels.
    enum_invoice_status.create(bind, checkfirst=True)

    # Normalise any legacy label still present in the column before the cast,
    # so the USING clause never fails on an unknown value.
    op.execute(
        """
        UPDATE invoice SET status = CASE status
            WHEN 'ALL' THEN 'All'
            WHEN 'ARCHIVED' THEN 'Archivé'
            WHEN 'TO_BE_TRAITED' THEN 'A Traiter'
            WHEN 'NEED_TO_CHECK' THEN 'Avoiriser'
            WHEN 'TO_BE_INVOICED' THEN 'A Facturer'
            WHEN 'INVOICED' THEN 'Facturer ticket'
            WHEN 'VALIDATED' THEN 'A Payer'
            WHEN 'VALIDATED_ONLY' THEN 'Payé'
            WHEN 'Valider avec paiement' THEN 'A Payer'
            WHEN 'Valider sans paiement' THEN 'Payé'
            ELSE status
        END
        """
    )

    # Convert the VARCHAR column to the enum type.
    op.execute(
        "ALTER TABLE invoice "
        "ALTER COLUMN status TYPE enuminvoicestatus "
        "USING status::enuminvoicestatus"
    )


def downgrade() -> None:
    """Revert ``invoice.status`` back to a plain ``VARCHAR`` column."""
    op.execute(
        "ALTER TABLE invoice "
        "ALTER COLUMN status TYPE VARCHAR(255) "
        "USING status::text"
    )
    enum_invoice_status.drop(op.get_bind(), checkfirst=True)
