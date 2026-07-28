"""align statusbuybackenum labels with enum values

Revision ID: c1a2b3d4e5f6
Revises: 5bfd47935906
Create Date: 2026-07-08 11:40:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'c1a2b3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '5bfd47935906'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Rename enum labels from member names to their business values.

    The buyback status column is now persisted using the enum *value*
    (e.g. "A Traiter") instead of the member name (e.g. "TO_BE_TRAITED"),
    to match the API contract. Renaming labels in place preserves existing
    rows.
    """
    op.execute("ALTER TYPE statusbuybackenum RENAME VALUE 'TO_BE_TRAITED' TO 'A Traiter'")
    op.execute("ALTER TYPE statusbuybackenum RENAME VALUE 'VALIDATED' TO 'Valider'")


def downgrade() -> None:
    """Revert enum labels back to the member names."""
    op.execute("ALTER TYPE statusbuybackenum RENAME VALUE 'A Traiter' TO 'TO_BE_TRAITED'")
    op.execute("ALTER TYPE statusbuybackenum RENAME VALUE 'Valider' TO 'VALIDATED'")
