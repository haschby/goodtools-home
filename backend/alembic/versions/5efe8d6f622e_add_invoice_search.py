"""add invoice search

Revision ID: 5efe8d6f622e
Revises: 14a3c1b31d42
Create Date: 2026-02-20 11:02:17.923507

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR


# revision identifiers, used by Alembic.
revision: str = '5efe8d6f622e'
down_revision: Union[str, Sequence[str], None] = '14a3c1b31d42'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade():
    # Enable pg_trgm
    op.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")

    # Add column search_vector
    op.add_column("invoice", sa.Column("search_vector", TSVECTOR()))

    # Create function
    op.execute("""
    CREATE FUNCTION invoice_search_vector_update() RETURNS trigger AS $$
    BEGIN
      NEW.search_vector :=
        to_tsvector('simple',
          coalesce(NEW.issuer_name,'') || ' ' ||
          coalesce(NEW.invoice_number,'') || ' ' ||
          coalesce(NEW.external_id,'')
        );
      RETURN NEW;
    END
    $$ LANGUAGE plpgsql;
    """)

    # Trigger
    op.execute("""
    CREATE TRIGGER invoice_search_vector_trigger
    BEFORE INSERT OR UPDATE ON invoice
    FOR EACH ROW EXECUTE FUNCTION invoice_search_vector_update();
    """)

    # Indexes
    op.execute("""
    CREATE INDEX idx_invoice_search_vector
    ON invoice USING GIN(search_vector);
    """)

    # Amount indexes
    op.execute("""
    CREATE INDEX idx_invoice_amount_ht ON invoice(amount_ht);
    CREATE INDEX idx_invoice_amount_ttc ON invoice(amount_ttc);
    """)

    # Trigram fuzzy indexes
    op.execute("""
    CREATE INDEX idx_invoice_invoice_number_trgm
    ON invoice USING GIN(invoice_number gin_trgm_ops);

    CREATE INDEX idx_invoice_issuer_name_trgm
    ON invoice USING GIN(issuer_name gin_trgm_ops);

    CREATE INDEX idx_invoice_external_id_trgm
    ON invoice USING GIN(external_id gin_trgm_ops);
    """)


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS invoice_search_vector_trigger ON invoice;")
    op.execute("DROP FUNCTION IF EXISTS invoice_search_vector_update;")

    op.drop_index("idx_invoice_search_vector", table_name="invoice")
    op.drop_index("idx_invoice_amount_ht", table_name="invoice")
    op.drop_index("idx_invoice_amount_ttc", table_name="invoice")
    op.drop_index("idx_invoice_invoice_number_trgm", table_name="invoice")
    op.drop_index("idx_invoice_issuer_name_trgm", table_name="invoice")
    op.drop_index("idx_invoice_external_id_trgm", table_name="invoice")

    op.drop_column("invoice", "search_vector")