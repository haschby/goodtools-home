from application.usecases.invoice.createInvoice import CreateInvoice
from application.usecases.invoice.getInvoice import GetInvoice
from application.usecases.invoice.updateInvoice import UpdateInvoice
from application.usecases.invoice.getInvoices import GetInvoices
from application.usecases.invoice.getLastInvoice import GetLastInvoice
from application.usecases.invoice.searchInvoice import SearchInvoice

class InvoiceFacade:
    def __init__(self,
        createInvoiceUsecase: CreateInvoice,
        getInvoiceUsecase: GetInvoice,
        updateInvoiceUsecase: UpdateInvoice,
        getAllInvoicesUsecase: GetInvoices,
        getLastInvoiceUsecase: GetLastInvoice,
        searchInvoiceUsecase: SearchInvoice
    ):
        self.createInvoiceUsecase = createInvoiceUsecase
        self.getInvoiceUsecase = getInvoiceUsecase
        self.updateInvoiceUsecase = updateInvoiceUsecase
        self.getAllInvoicesUsecase = getAllInvoicesUsecase
        self.getLastInvoiceUsecase = getLastInvoiceUsecase
        self.searchInvoiceUsecase = searchInvoiceUsecase