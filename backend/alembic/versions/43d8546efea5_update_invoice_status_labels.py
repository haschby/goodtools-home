"""update_invoice_status_labels

Revision ID: 43d8546efea5
Revises: bb82b0c2c632
Create Date: 2026-09-03 20:31:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '43d8546efea5'
down_revision: Union[str, Sequence[str], None] = 'bb82b0c2c632'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        "UPDATE invoice SET status = 'A Payer' "
        "WHERE status = 'Valider avec paiement'"
    )
    op.execute(
        "UPDATE invoice SET status = 'Payé' "
        "WHERE status = 'Valider sans paiement'"
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        "UPDATE invoice SET status = 'Valider avec paiement' "
        "WHERE status = 'A Payer'"
    )
    op.execute(
        "UPDATE invoice SET status = 'Valider sans paiement' "
        "WHERE status = 'Payé'"
    )
