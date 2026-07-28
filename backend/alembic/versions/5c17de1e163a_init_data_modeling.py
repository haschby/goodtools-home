"""Init Data Modeling

Revision ID: 5c17de1e163a
Revises: 
Create Date: 2026-07-28 21:34:50.079717

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = '5c17de1e163a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# On pilote nous-mêmes la création des types ENUM (create_type=False) pour
# éviter la double création implicite déclenchée par op.create_table, et pour
# gérer proprement statusworkflow qui est partagé par workflow / workflow_step.
status_buyback_enum = postgresql.ENUM(
    'A Traiter', 'Valider', name='statusbuybackenum', create_type=False
)
status_workflow_enum = postgresql.ENUM(
    'PENDING', 'PROCESSING', 'COMPLETED', 'FAILED', 'SKIP', 'ABORT',
    name='statusworkflow', create_type=False,
)
role_enum = postgresql.ENUM('ADMIN', name='role', create_type=False)


def upgrade() -> None:
    """Upgrade schema."""
    bind = op.get_bind()
    status_buyback_enum.create(bind, checkfirst=True)
    status_workflow_enum.create(bind, checkfirst=True)
    role_enum.create(bind, checkfirst=True)

    # --- buyback ---------------------------------------------------------
    op.create_table(
        'buyback',
        sa.Column(
            'status',
            status_buyback_enum,
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

    # --- user ------------------------------------------------------------
    op.create_table(
        'user',
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column(
            'role',
            role_enum,
            nullable=False,
        ),
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
        sa.UniqueConstraint('email'),
    )

    # --- invoice ---------------------------------------------------------
    op.create_table(
        'invoice',
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('path', sa.Text(), nullable=False),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('invoice_number', sa.String(length=255), nullable=True),
        sa.Column('invoice_date', sa.Date(), nullable=True),
        sa.Column('amount_ht', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('amount_ttc', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('amount_tva', sa.Numeric(precision=10, scale=2), nullable=True),
        sa.Column('issuer_name', sa.String(length=500), nullable=True),
        sa.Column('construction_site_address', sa.String(length=500), nullable=True),
        sa.Column('gc_booking', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=255), nullable=False),
        sa.Column('images', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('extracted_data', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('comments', sa.Text(), nullable=True),
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
        sa.UniqueConstraint('external_id'),
    )
    op.create_index('ix_invoice_external_id', 'invoice', ['external_id'], unique=True)
    op.create_index(
        'ix_invoices_created_at_id', 'invoice', ['created_at', 'id'], unique=False
    )
    op.create_index(
        'ix_invoices_status_created_at_id',
        'invoice',
        ['status', 'created_at', 'id'],
        unique=False,
    )

    # --- workflow --------------------------------------------------------
    op.create_table(
        'workflow',
        sa.Column('ref_pulling', sa.String(length=255), nullable=False),
        sa.Column('provider', sa.String(length=255), nullable=False),
        sa.Column(
            'status',
            status_workflow_enum,
            nullable=False,
        ),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('message', sa.String(length=255), nullable=True),
        sa.Column('params', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
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

    # --- workflow_step ---------------------------------------------------
    op.create_table(
        'workflow_step',
        sa.Column('workflow_id', sa.String(length=36), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column(
            'status',
            status_workflow_enum,
            nullable=False,
        ),
        sa.Column('params', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('message', sa.String(length=255), nullable=True),
        sa.Column('ended_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column(
            'id',
            sa.String(length=36),
            server_default=sa.text('gen_random_uuid()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['workflow_id'], ['workflow.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('id'),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('workflow_step')
    op.drop_table('workflow')

    op.drop_index('ix_invoices_status_created_at_id', table_name='invoice')
    op.drop_index('ix_invoices_created_at_id', table_name='invoice')
    op.drop_index('ix_invoice_external_id', table_name='invoice')
    op.drop_table('invoice')

    op.drop_table('user')

    op.drop_index('ix_buybacks_status_created_at_id', table_name='buyback')
    op.drop_index('ix_buybacks_created_at_id', table_name='buyback')
    op.drop_table('buyback')

    bind = op.get_bind()
    sa.Enum(name='role').drop(bind, checkfirst=True)
    sa.Enum(name='statusworkflow').drop(bind, checkfirst=True)
    sa.Enum(name='statusbuybackenum').drop(bind, checkfirst=True)
