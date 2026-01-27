from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from domain.dtos.invoiceDto import InvoiceResponseSchema

class OCRResponseSchema(BaseModel):
    InvoiceResponseSchema: InvoiceResponseSchema