from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class BaseInvoiceSchema(BaseModel):
    id: Optional[str] = None
    
    class Config:
        from_attributes = True

class InvoiceCreateSchema(BaseInvoiceSchema):
    name: Optional[str] = None
    path: Optional[str] = None
    external_id: Optional[str] = None
    comments: Optional[str] = None
    gc_booking: Optional[str | None] = None   
    amount_ttc: Optional[float] = None
    amount_ht: Optional[float] = None
    amount_tva: Optional[float] = None
    issuer_name: Optional[str] = None
    construction_site_address: Optional[str] = None
    invoice_number: Optional[str | None] = None
    invoice_date: Optional[date | None] = None
    status: Optional[str] = None
    images: Optional[list] = []
    extracted_data: Optional[dict] = {}
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
        
    class Config:
        from_attributes = True

class InvoiceUpdateSchema(BaseInvoiceSchema):
    name: Optional[str] = None
    path: Optional[str] = None
    amount_ttc: Optional[float] = None
    amount_ht: Optional[float] = None
    amount_tva: Optional[float] = None
    gc_booking: Optional[str | None] = None
    issuer_name: Optional[str | None] = None
    comments: Optional[str] = None
    status: Optional[str] = None
    
    class Config:
        from_attributes = True

class InvoiceResponseSchema(BaseInvoiceSchema):
    name: str | None    
    path: str | None
    gc_booking: str | None
    external_id: str | None
    comments: str | None
    amount_ttc: float | None
    amount_ht: float | None
    amount_tva: float | None
    issuer_name: str | None
    construction_site_address: str | None   
    invoice_number: str | None
    invoice_date: date | None
    status: str | None
    images: list | None
    extracted_data: dict | None
    created_at: datetime | None
    updated_at: datetime | None
    images_url: Optional[str] = None
        
    class Config:
        from_attributes = True