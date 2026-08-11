from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, Body, Request
from typing import Optional, List

from application.containers.appContainer import AppContainer
from application.ports.baseUsecase import BaseUsecase
from domain.models.invoice import EnumInvoiceStatus

from application.ports.orchestrator.workflowLauncher import WorkflowLauncher
from application.dtos.workflow import SyncUpdateInvoiceToPennylaneCommand, SyncInvoiceToGcCommand, WorkflowCommand

from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import ( 
    InvoiceResponseSchema, 
    InvoiceCreateSchema, 
    InvoiceUpdateSchema,
    InvoiceDetailResponseSchema,
    InvoiceListResponseSchema,
    InvoiceUpdateResponseSchema
)

INVOICES_STATUS_DICT = {
    EnumInvoiceStatus.ALL: "All",
    EnumInvoiceStatus.TBD: "TBD",
    EnumInvoiceStatus.TO_BE_TRAITED: "A Traiter",
    EnumInvoiceStatus.NEED_TO_CHECK: "Avoiriser",
    EnumInvoiceStatus.TO_BE_INVOICED: "A Facturer",
    EnumInvoiceStatus.INVOICED: "Facturer ticket",
    EnumInvoiceStatus.VALIDATED: "Valider",
}

def invoice_routes() -> APIRouter:
    
    router = APIRouter(
        prefix="/client/invoice",
        tags=["invoice"]
    )
    
    @router.get(
    '/count',
    response_model=BaseResponseSchema[int],
    status_code=201)
    @inject
    async def count(
        repository: any = Depends(
            Provide[AppContainer.invoice_container.repository]
        )
    ):
        number = await repository.count()
        return BaseResponseSchema.response(
            message="Total records found",
            status_code=201,
            data=number
        )
    
    @router.get(
    '/all',
    response_model=InvoiceListResponseSchema,
    status_code=201)
    @inject
    async def invoices(
        status: Optional[str] = Query(default="All", description="Filter invoices by status"),
        page: Optional[int] = Query(default=1, description="Page Selector"),
        limit: Optional[int] = Query(default=30, description="Limit Selector"),
        query: Optional[str] = Query(default=None, description="Query Selector"),
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.getAllInvoicesUsecase]
        )
    ):
        params = {
            "status": status,
            "page": page,
            "limit": limit,
            "query": query
        }
        
        return await useCase.execute(params)
    

    @router.post(
    '/',
    response_model=InvoiceUpdateResponseSchema,
    status_code=201)
    @inject
    async def create(
        new_invoice: InvoiceCreateSchema,
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.createInvoiceUsecase]
        )
    ):
        return await useCase.execute([new_invoice])
    
    
    @router.get(
    '/{id:str}',
    response_model=InvoiceDetailResponseSchema,
    status_code=201)
    @inject
    async def invoice(
        id: str,
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.getInvoiceUsecase]
        )
    ):
        return await useCase.execute(id)
    
    
    @router.patch(
    '/{id:str}',
    response_model=InvoiceUpdateResponseSchema,
    status_code=201)
    @inject
    async def update(
        id: str,
        update_invoice: InvoiceUpdateSchema,
        background_tasks: BackgroundTasks,
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.updateInvoiceUsecase]
        ),
        orchestrator: WorkflowLauncher = Depends(
            Provide[AppContainer.orchestrator_container.localWorkflowLauncher]
        )
    ):
        
        try:
            response = await useCase.execute([update_invoice])
        except Exception as e:
            print('@ERROR', e)
            return BaseResponseSchema.response(
                message=f"Error updating invoice: {str(e)}",
                status_code=500,
                data=None
            )
        print('@RESPONSE', response.data.status)
        print('@ENUM_INVOICE_STATUS', EnumInvoiceStatus.VALIDATED.value)
        if response.data.status == EnumInvoiceStatus.VALIDATED.value:
            command = SyncUpdateInvoiceToPennylaneCommand(
                workflow_id='INTERNAL',
                workflow_name="updateInvoiceToPennylaneWorkflow",
                invoice_id=id
            )
            background_tasks.add_task(orchestrator.startWorkflow, command)

            gc_command = SyncInvoiceToGcCommand(
                workflow_id='INTERNAL',
                workflow_name="syncInvoiceToGcWorkflow",
                invoice_id=id
            )
            background_tasks.add_task(orchestrator.startWorkflow, gc_command)
        elif id in getattr(useCase, "gc_booking_added_ids", []):
            gc_command = SyncInvoiceToGcCommand(
                workflow_id='INTERNAL',
                workflow_name="syncInvoiceToGcWorkflow",
                invoice_id=id
            )
            background_tasks.add_task(orchestrator.startWorkflow, gc_command)
        
        return response
    
    
    @router.post(
    '/search',
    response_model=BaseResponseSchema[InvoiceResponseSchema],
    status_code=201)
    @inject
    async def search(
        q: str,
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.searchInvoiceUsecase]
        )
    ):
        return await useCase.execute(q)
    

    @router.patch(
    '/bulk/update/{status:str}',
    response_model=InvoiceUpdateResponseSchema,
    status_code=201)
    @inject
    async def bulk(
        status: str,
        ids: list[str],
        background_tasks: BackgroundTasks,
        gc_booking: Optional[str] = Query(default=None),
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.updateInvoiceUsecase]
        ),
        orchestrator: WorkflowLauncher = Depends(
            Provide[AppContainer.orchestrator_container.localWorkflowLauncher]
        )
    ):

        normalized_status = None if status.lower() == "none" else status
        fields = {}
        if normalized_status:
            fields["status"] = normalized_status
        if gc_booking:
            fields["gc_booking"] = gc_booking

        if not fields:
            raise HTTPException(
                status_code=400,
                detail="At least one of 'status' or 'gc_booking' must be provided",
            )

        invoice_updates = [
            InvoiceUpdateSchema(id=id, **fields)
            for id in ids
        ]
        
        updated_invoices = await useCase.execute(invoice_updates)
        
        jobs: List[WorkflowCommand] = []
        if normalized_status == EnumInvoiceStatus.VALIDATED.value:
            for invoice_id in ids:
                command = SyncUpdateInvoiceToPennylaneCommand(
                    workflow_id='UpdatePennylane',
                    workflow_name="updateInvoiceToPennylaneWorkflow",
                    invoice_id=invoice_id
                )

                gc_command = SyncInvoiceToGcCommand(
                    workflow_id='SyncGoodCollect',
                    workflow_name="syncInvoiceToGcWorkflow",
                    invoice_id=invoice_id
                )
                jobs.append(command)
                jobs.append(gc_command)
        else:
            for invoice_id in getattr(useCase, "gc_booking_added_ids", []):
                gc_command = SyncInvoiceToGcCommand(
                    workflow_id='SyncGoodCollect',
                    workflow_name="syncInvoiceToGcWorkflow",
                    invoice_id=invoice_id
                )
                jobs.append(gc_command)
                
        if jobs != []:
            orchestrator.registerWorkflows(jobs)    
            await orchestrator.launchWorkflows()
            
        return updated_invoices
    
    return router