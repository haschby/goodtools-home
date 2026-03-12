from dependency_injector import containers, providers
from application.ports.orchestrator.workflowLauncher import WorkflowLauncher
from application.orchestrator.syncPennyLaneWorkflow import SyncPennyLaneWorkflow
from application.orchestrator.syncUpdatInvoiceToPennylane import SyncUpdateInvoiceToPennylane
from infrastructure.db.workflowRepository import WorkflowRepositoryImpl
from infrastructure.orchestrator.localWorkflowLauncher import LocalWorkflowLauncher
from application.containers.orchestrator.activitiesContainer import ActivitiesContainer

class OrchestratorContainer(containers.DeclarativeContainer):

    pennylane_gateway = providers.Dependency()
    storage = providers.Dependency()
     
    invoice_container = providers.DependenciesContainer()
    workflow_container = providers.DependenciesContainer()
    activities_container = providers.DependenciesContainer()
    
    synchronize_pennylane_workflow = providers.Factory(
        SyncPennyLaneWorkflow,
        create_workflow_usecase=activities_container.createWorkflowSync,
        update_workflow_usecase=workflow_container.workflowFacade.provided.updateWorkflowUsecase,
        fetch_pennylane_supplier_invoices_usecase=activities_container.fetchPennyLaneSupplierInvoices,
        store_pdf_invoice_usecase=activities_container.storePDFInvoice,
        create_invoice_usecase=invoice_container.invoiceFacade.provided.createInvoiceUsecase,
        # update_workflow_usecase=activities.updateWorkflowSync,
        # store_pdf_invoice_usecase=activities.storePDFInvoice,
        # create_invoice_usecase=invoice_container.invoiceFacade.provided.createInvoiceUsecase
    )
    
    update_invoice_to_pennylane_workflow = providers.Factory(
        SyncUpdateInvoiceToPennylane,
        create_workflow_usecase=activities_container.createWorkflowSync,
        update_workflow_usecase=workflow_container.workflowFacade.provided.updateWorkflowUsecase,
        update_pennylane_supplier_invoice_usecase=activities_container.updatePennyLaneSupplierInvoice,
        search_invoice_usecase=invoice_container.invoiceFacade.provided.searchInvoiceUsecase
    )
    
    _workflows = providers.Dict(
        syncPennyLaneWorkflow=synchronize_pennylane_workflow,
        updateInvoiceToPennylaneWorkflow=update_invoice_to_pennylane_workflow
    )
    
    localWorkflowLauncher = providers.Factory(
        LocalWorkflowLauncher,
        workflows=_workflows
    )