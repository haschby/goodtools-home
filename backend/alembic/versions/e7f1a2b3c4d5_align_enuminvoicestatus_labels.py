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
    """Reconcile ``invoice.status`` with the ORM enum, whatever the DB state.

    Historically ``invoice.status`` was created as a plain ``VARCHAR`` (see the
    init migration), while the ORM maps it as an enum column using the business
    *values* (``EnumInvoiceStatus`` with ``use_values=True``). This migration
    reconciles the database with the ORM by ensuring the Postgres enum type
    exists with the final business labels and that the column uses it.

    An earlier, buggy revision of this file ran ``ALTER TYPE ... RENAME VALUE``
    on a non-existent type and crashed mid-way in production. To be safe when
    re-run against a database left in *any* intermediate state, every step
    below is idempotent:

    * the enum type is created only if missing, and any legacy member label
      still present on the type is renamed to its final business value;
    * the column values are normalised only while the column is still text;
    * the column is converted to the enum type only if it is not already so.
    """
    bind = op.get_bind()

    # 1. Ensure the enum type exists. If a previous partial run created it with
    #    the ORM member *names* (ALL, ARCHIVED, ...) instead of the business
    #    values, rename each label to its final value. Both operations are
    #    conditional so the migration is safe on a fresh or partially migrated
    #    database alike.
    op.execute(
        """
        DO $$
        DECLARE
            legacy_to_final CONSTANT text[][] := ARRAY[
                ['ALL', 'All'],
                ['ARCHIVED', 'Archivé'],
                ['TO_BE_TRAITED', 'A Traiter'],
                ['NEED_TO_CHECK', 'Avoiriser'],
                ['TO_BE_INVOICED', 'A Facturer'],
                ['INVOICED', 'Facturer ticket'],
                ['VALIDATED', 'A Payer'],
                ['VALIDATED_ONLY', 'Payé']
            ];
            pair text[];
        BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'enuminvoicestatus') THEN
                CREATE TYPE enuminvoicestatus AS ENUM (
                    'All', 'TBD', 'Archivé', 'A Traiter', 'Avoiriser',
                    'A Facturer', 'Facturer ticket', 'A Payer', 'Payé'
                );
            ELSE
                -- Rename any legacy member label that survived a partial run.
                FOREACH pair SLICE 1 IN ARRAY legacy_to_final LOOP
                    IF EXISTS (
                        SELECT 1
                        FROM pg_enum e
                        JOIN pg_type t ON t.oid = e.enumtypid
                        WHERE t.typname = 'enuminvoicestatus'
                          AND e.enumlabel = pair[1]
                    ) THEN
                        EXECUTE format(
                            'ALTER TYPE enuminvoicestatus RENAME VALUE %L TO %L',
                            pair[1], pair[2]
                        );
                    END IF;
                END LOOP;
            END IF;
        END
        $$;
        """
    )

    # 2. If the column is still text, normalise any legacy label and convert it
    #    to the enum type. If it is already the enum type, there is nothing to
    #    do (the migration has effectively already been applied).
    op.execute(
        """
        DO $$
        DECLARE
            col_type text;
        BEGIN
            SELECT format_type(a.atttypid, a.atttypmod)
              INTO col_type
              FROM pg_attribute a
              JOIN pg_class c ON c.oid = a.attrelid
             WHERE c.relname = 'invoice'
               AND a.attname = 'status'
               AND a.attnum > 0
               AND NOT a.attisdropped;

            IF col_type IS DISTINCT FROM 'enuminvoicestatus' THEN
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
                END;

                ALTER TABLE invoice
                    ALTER COLUMN status TYPE enuminvoicestatus
                    USING status::enuminvoicestatus;
            END IF;
        END
        $$;
        """
    )


def downgrade() -> None:
    """Revert ``invoice.status`` back to a plain ``VARCHAR`` column."""
    op.execute(
        "ALTER TABLE invoice "
        "ALTER COLUMN status TYPE VARCHAR(255) "
        "USING status::text"
    )
    enum_invoice_status.drop(op.get_bind(), checkfirst=True)
