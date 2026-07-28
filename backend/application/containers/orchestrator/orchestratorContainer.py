from dependency_injector import containers, providers
from application.ports.orchestrator.workflowLauncher import WorkflowLauncher
from application.orchestrator.syncPennyLaneWorkflow import SyncPennyLaneWorkflow
from application.orchestrator.syncUpdatInvoiceToPennylane import SyncUpdateInvoiceToPennylane
from application.orchestrator.syncBuybackToGcWorkflow import SyncBuybackToGcWorkflow
from infrastructure.db.workflowRepository import WorkflowRepositoryImpl
from infrastructure.orchestrator.localWorkflowLauncher import LocalWorkflowLauncher
from application.containers.orchestrator.activitiesContainer import ActivitiesContainer

from infrastructure.db.engine import Database 

class OrchestratorContainer(containers.DeclarativeContainer):

    pennylane_gateway = providers.Dependency()
    storage = providers.Dependency()
    main_session = providers.Dependency()
    goodcollect_gateway = providers.Dependency()
     
    invoice_container = providers.DependenciesContainer()
    workflow_container = providers.DependenciesContainer()
    activities_container = providers.DependenciesContainer()
    
    synchronize_pennylane_workflow = providers.Factory(
        SyncPennyLaneWorkflow,
        session_factory=main_session,
        fetch_pennylane_supplier_invoices_usecase=activities_container.fetchPennyLaneSupplierInvoices,
        store_pdf_invoice_usecase=activities_container.storePDFInvoice,
        create_invoice_usecase=invoice_container.invoiceFacade.provided.createInvoiceUsecase,
    )
    
    update_invoice_to_pennylane_workflow = providers.Factory(
        SyncUpdateInvoiceToPennylane,
        session_factory=main_session,
        update_pennylane_supplier_invoice_usecase=activities_container.updatePennyLaneSupplierInvoice,
        get_invoice_usecase=invoice_container.invoiceFacade.provided.getInvoiceUsecase
    )
    
    sync_buyback_to_gc_workflow = providers.Factory(
        SyncBuybackToGcWorkflow,
        session_factory=main_session,
        goodcollect_gateway=goodcollect_gateway,
    )
    
    _workflows = providers.Dict(
        syncPennyLaneWorkflow=synchronize_pennylane_workflow,
        updateInvoiceToPennylaneWorkflow=update_invoice_to_pennylane_workflow,
        syncBuybackToGcWorkflow=sync_buyback_to_gc_workflow,
    )
    
    localWorkflowLauncher = providers.Factory(
        LocalWorkflowLauncher,
        workflows=_workflows
    )