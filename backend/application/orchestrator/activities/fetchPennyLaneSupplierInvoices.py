from application.ports.orchestrator.baseActivity import BaseActivity
from application.ports.providers.accountingGateway import AccountingGateway
from application.facades.invoiceFacade import InvoiceFacade
from application.dtos.invoiceDto import InvoiceResponseSchema
from domain.mappers.invoiceMapper import InvoiceMapper
from datetime import datetime, timezone

class FetchPennyLaneSupplierInvoices(BaseActivity):
    def __init__(
        self,
        pennylane_gateway: AccountingGateway,
        get_last_invoice_usecase: BaseActivity,
    ) -> None:
        self.pennylane_gateway = pennylane_gateway
        self.get_last_invoice_usecase = get_last_invoice_usecase
        
    async def execute(self) -> list[InvoiceResponseSchema] | None:
        
        cursor = None
        last_invoice_id = await self.get_last_invoice_usecase.execute()
        
        if last_invoice_id:
            cursor = { "id": last_invoice_id }
        
        supplier_invoices = await self.pennylane_gateway.fetch_supplier_invoices(cursor=cursor)
        invoices = supplier_invoices.get("items", [])
        invoices_to_treat = []
        for invoice in invoices:
            date = datetime.fromisoformat(invoice.get("created_at"))
            if date.tzinfo is None:
                date = date.replace(tzinfo=timezone.utc)
            
            threshold_date = datetime(2026, 3, 1, tzinfo=timezone.utc)
            if date >= threshold_date:
                invoices_to_treat.append(invoice)    
            # if invoice.get("accounting_status") == "validation_needed":
            
        
        if not invoices_to_treat:
            return None
        
        await self._enrich_supplier_info(invoices_to_treat)
        return InvoiceMapper.from_pennylane_list(invoices_to_treat)
    
    async def _enrich_supplier_info(self, invoices: list[dict]) -> list[dict]:
        supplier_ids = {
            invoice['supplier']['id']
            for invoice in invoices
            if invoice.get("supplier", {})
            and invoice.get("supplier", {}).get("id")
        }
        
        if not supplier_ids:
            for invoice in invoices:
                invoice.update({"supplier": None})
                
            return invoices
        
        suppliers_response = await self.pennylane_gateway.fetch_supplier_info(list(supplier_ids))
        suppliers = suppliers_response.get("items", []) if suppliers_response else []
        
        suppliers_mapping = {
            supplier['id']: supplier['name']
            for supplier in suppliers
            if supplier.get("id")
        }
        
        for invoice in invoices:
            supplier = invoice.get("supplier", {})
            if supplier and supplier.get("id"):
                invoice.update({"supplier": suppliers_mapping.get(supplier.get("id"))})
            else:
                invoice.update({"supplier": None})
        
        return invoices
    
    
    
    
    
    
    