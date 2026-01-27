from .baseModel import BaseModel
from .columns import (
    StringColumn, TextColumn, JSONBColumn,
    NumericColumn, DateColumn, EnumColumn
)
from typing import List, Dict, BinaryIO
from datetime import date
from enum import Enum

class EnumInvoiceStatus(Enum):
    ALL = "All"
    TBD = "TBD"
    TO_BE_TRAITED = "A Traiter"
    NEED_TO_CHECK = "Avoiriser"
    TO_BE_INVOICED = "A Facturer"
    INVOICED = "Facturer ticket"
    VALIDATED = "Valider"

class Invoice(BaseModel):
    prefix: str = "INV"
    
    name: str = StringColumn(length=255, nullable=False)
    path: str = TextColumn(nullable=False)
    invoice_number: str = StringColumn(length=255, nullable=True)
    invoice_date: date = DateColumn(nullable=True)
    amount_ht: float = NumericColumn(nullable=True)
    amount_ttc: float = NumericColumn(nullable=True)
    amount_tva: float = NumericColumn(nullable=True)
    issuer_name: str = StringColumn(length=500, nullable=True)
    construction_site_address: str = StringColumn(length=500, nullable=True)
    gc_booking: str = StringColumn(length=255, nullable=True)
    status: str = StringColumn(length=255, nullable=False)
    images: list = JSONBColumn(nullable=True)
    extracted_data: dict = JSONBColumn(nullable=True)
    comments: str = TextColumn(nullable=True)
    
    def __post_init__(self):
        if self.status:
            self.status = EnumInvoiceStatus(self.status)