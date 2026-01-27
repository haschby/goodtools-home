from domain.models.invoice import Invoice
from domain.ports.baseRepository import BaseRepositoryPort

class InvoiceRepositoryPort(BaseRepositoryPort[Invoice]):
    pass