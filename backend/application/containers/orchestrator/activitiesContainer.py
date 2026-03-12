from dependency_injector import containers, providers
from application.orchestrator.activities.fetchPennyLaneSupplierInvoices import FetchPennyLaneSupplierInvoices
from application.orchestrator.activities.createWorkflowSync import CreateWorkflowSync
from application.orchestrator.activities.updateWorkflowSync import UpdateWorkflowSync
from application.orchestrator.activities.storePDFInvoice import StorePDFInvoice
from application.orchestrator.activities.createWorkflowStepSync import CreateWorkflowStepSync
from application.orchestrator.activities.getExternalInvoiceIdSync import GetExternalInvoiceIdSync
from application.orchestrator.activities.updatePennyLaneSupplierInvoice import UpdatePennyLaneSupplierInvoice

class ActivitiesContainer(containers.DeclarativeContainer):
    
    pennylane_gateway = providers.Dependency()
    storage = providers.Dependency()
    invoice_container = providers.DependenciesContainer()
    workflow_container = providers.DependenciesContainer()
    
    storePDFInvoice = providers.Factory(
        StorePDFInvoice,
        storage=storage
    )
    
    # createWorkflowStepSync = providers.Factory(
    #     CreateWorkflowStepSync,
    #     createWorkflowStepUsecase=workflow_container.workflowFacade.createWorkflowStepUsecase
    # )
    
    fetchPennyLaneSupplierInvoices = providers.Factory(
        FetchPennyLaneSupplierInvoices,
        pennylane_gateway=pennylane_gateway,
        get_last_invoice_usecase=invoice_container.getLastInvoiceUsecase
    )
    
    createWorkflowSync = providers.Factory(
        CreateWorkflowSync,
        createWorkflowUsecase=workflow_container.workflowFacade.provided.createWorkflowUsecase
    )
    
    updateWorkflowSync = providers.Factory(
        UpdateWorkflowSync,
        updateWorkflowUsecase=workflow_container.workflowFacade.provided.updateWorkflowUsecase
    )
    
    updatePennyLaneSupplierInvoice = providers.Factory(
        UpdatePennyLaneSupplierInvoice,
        accounting_gateway=pennylane_gateway
    )
    
    getExternalInvoiceIdSync = providers.Factory(
        GetExternalInvoiceIdSync,
        search_invoice_usecase=invoice_container.invoiceFacade.provided.searchInvoiceUsecase
    )
