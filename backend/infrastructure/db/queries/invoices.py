QUERY_GET_ALL_INVOICES = """
SELECT
id, name, external_id, invoice_number, invoice_date, amount_ht,
amount_ttc, amount_tva, issuer_name, gc_booking, status, created_at, updated_at
FROM invoice
"""

QUERY_GET_LAST_INVOICE_ID = """
SELECT
external_id
FROM invoice
ORDER BY external_id DESC
LIMIT 1
"""

QUERY_GET_INVOICE_BY_ID = """
SELECT
id, external_id
FROM invoice
"""

QUERY_GET_INVOICE_ID = """
SELECT
id, name, path, external_id, invoice_number, amount_ht,
amount_ttc, amount_tva, issuer_name, gc_booking, status, 
comments
FROM invoice
"""


