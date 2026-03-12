from dependency_injector import containers, providers
from infrastructure.proxies.loggerProxy import LoggedRepoProxy
from infrastructure.db.invoiceRepository import InvoiceRepositoryImpl

from domain.services.invoiceService import InvoiceService

from application.usecases.invoice.createInvoice import CreateInvoice
from application.usecases.invoice.getInvoice import GetInvoice
from application.usecases.invoice.updateInvoice import UpdateInvoice
from application.usecases.invoice.getInvoices import GetInvoices
from application.usecases.invoice.getLastInvoice import GetLastInvoice
from application.usecases.invoice.searchInvoice import SearchInvoice

from application.facades.invoiceFacade import InvoiceFacade

class InvoiceContainer(containers.DeclarativeContainer):
    
    session = providers.Dependency()
    storage = providers.Dependency()
    pennylane_gateway = providers.Dependency()
    logger = providers.Dependency()
    
    repository = providers.Factory(
        InvoiceRepositoryImpl, 
        session=session
    )
    
    logged_repository = providers.Factory(
        LoggedRepoProxy,
        repo=repository,
        logger=logger
    )
    
    service = providers.Factory(
        InvoiceService,
        invoiceRepository=logged_repository,
        storage=storage
    )
    
    createInvoiceUsecase = providers.Factory(
        CreateInvoice,
        invoiceService=service
    )
    
    getInvoiceUsecase = providers.Factory(
        GetInvoice,
        invoiceService=service,
        accountingGateway=pennylane_gateway
    )
    
    updateInvoiceUsecase = providers.Factory(
        UpdateInvoice,
        invoiceService=service
    )
    
    getAllInvoicesUsecase = providers.Factory(
        GetInvoices,
        invoiceService=service
    )
    
    getLastInvoiceUsecase = providers.Factory(
        GetLastInvoice,
        invoiceService=service
    )
    
    searchInvoiceUsecase = providers.Factory(
        SearchInvoice,
        invoiceService=service
    )
    
    invoiceFacade = providers.Factory(
        InvoiceFacade,
        createInvoiceUsecase=createInvoiceUsecase,
        getInvoiceUsecase=getInvoiceUsecase,
        updateInvoiceUsecase=updateInvoiceUsecase,
        getAllInvoicesUsecase=getAllInvoicesUsecase,
        getLastInvoiceUsecase=getLastInvoiceUsecase,
        searchInvoiceUsecase=searchInvoiceUsecase
    )