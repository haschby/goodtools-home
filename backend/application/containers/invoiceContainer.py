from dependency_injector import containers, providers
from infrastructure.db.invoiceRepository import InvoiceRepositoryImpl
from domain.services.invoiceService import InvoiceService
from application.usecases.invoice.createInvoice import CreateInvoice
from application.usecases.invoice.getInvoice import GetInvoice
from application.usecases.invoice.updateInvoice import UpdateInvoice
from application.usecases.invoice.getInvoices import GetInvoices

class InvoiceContainer(containers.DeclarativeContainer):
    
    postgres = providers.Dependency()
    storage = providers.Dependency()
    
    repository = providers.Factory(
        InvoiceRepositoryImpl, 
        session=postgres
    )
    
    service = providers.Factory(
        InvoiceService,
        invoiceRepository=repository,
        storage=storage
    )
    
    createInvoiceUsecase = providers.Factory(
        CreateInvoice,
        invoiceService=service
    )
    
    getInvoiceUsecase = providers.Factory(
        GetInvoice,
        invoiceService=service
    )
    
    updateInvoiceUsecase = providers.Factory(
        UpdateInvoice,
        invoiceService=service
    )
    
    getAllInvoicesUsecase = providers.Factory(
        GetInvoices,
        invoiceService=service
    )