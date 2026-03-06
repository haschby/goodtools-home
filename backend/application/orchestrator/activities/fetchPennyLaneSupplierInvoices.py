from application.ports.orchestrator.baseActivity import BaseActivity
from application.ports.providers.accountingGateway import AccountingGateway
from application.facades.invoiceFacade import InvoiceFacade
from application.dtos.invoiceDto import InvoiceResponseSchema
from domain.mappers.invoiceMapper import InvoiceMapper

class FetchPennyLaneSupplierInvoices(BaseActivity):
    def __init__(
        self,
        pennylane_gateway: AccountingGateway,
        get_last_invoice_usecase: BaseActivity,
    ) -> None:
        self.pennylane_gateway = pennylane_gateway
        self.get_last_invoice_usecase = get_last_invoice_usecase
        
    async def execute(self) -> list[InvoiceResponseSchema] | None:
        last_invoice_id = await self.get_last_invoice_usecase.execute()
        cursor = None
        if last_invoice_id:
            cursor = {
                "id": last_invoice_id
            }
        
        supplier_invoices = await self.pennylane_gateway.fetch_supplier_invoices(cursor=cursor)
        invoices = supplier_invoices.get("items", [])
        
        if invoices:
            supplier_ids = []
            for invoice in invoices:
                if invoice.get("supplier", {}) is not None:
                    supplier_ids.append(invoice.get("supplier", {}).get("id"))
                    
            if supplier_ids:
                suppliers = await self.pennylane_gateway.fetch_supplier_info(list(supplier_ids))
                suppliers = suppliers.get("items", []) if suppliers else []
            
            if suppliers:
                for supplier in suppliers:
                    if supplier.get("id"):
                        supplier.update({"name": supplier.get("name")})
                    else:
                        supplier.update({"name": None})
                
                suppliers_dict = {supplier.get("id"): supplier.get("name") for supplier in suppliers}
                for invoice in invoices:
                    if invoice.get("supplier", {}) is not None:
                        invoice.update({"supplier": suppliers_dict.get(invoice.get("supplier", {}).get("id"))})
                    else:
                        invoice.update({"supplier": None})
                    
            return InvoiceMapper.from_pennylane_list(invoices)
        return None