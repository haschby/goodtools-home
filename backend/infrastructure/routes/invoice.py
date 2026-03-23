from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query, BackgroundTasks, Body
from typing import Optional

from application.containers.appContainer import AppContainer
from application.ports.baseUsecase import BaseUsecase
from domain.models.invoice import EnumInvoiceStatus

from application.ports.orchestrator.workflowLauncher import WorkflowLauncher
from application.dtos.workflow import SyncUpdateInvoiceToPennylaneCommand

from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import ( 
    InvoiceResponseSchema, 
    InvoiceCreateSchema, 
    InvoiceUpdateSchema,
    InvoiceBulkUpdateSchema
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
    status_code=201 )
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
    response_model=BaseResponseSchema[InvoiceResponseSchema],
    status_code=201)
    @inject
    async def invoices(
        status: Optional[str] = Query(default="All", description="Filter invoices by status"),
        cursor: Optional[str|None] = Query(default=None, description="Cursor Selector"),
        id: Optional[str|None] = Query(default=None, description="ID Selector"),
        limit: Optional[int] = Query(default=50, description="Limit Selector"),
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.getAllInvoicesUsecase]
        )
    ):
        params = {
            "status": status,
            "cursor": {
                "created_at": cursor,
                "id": id
            },
            "limit": limit
        }
        return await useCase.execute(params)

    @router.post(
    '/',
    response_model=BaseResponseSchema[InvoiceResponseSchema],
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
    response_model=BaseResponseSchema[InvoiceResponseSchema],
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
    response_model=BaseResponseSchema[InvoiceResponseSchema],
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
        updated_invoice = await useCase.execute(update_invoice)
        if updated_invoice['data'].status == EnumInvoiceStatus.VALIDATED.value:
            command = SyncUpdateInvoiceToPennylaneCommand(
                workflow_id='INTERNAL',
                workflow_name="updateInvoiceToPennylaneWorkflow",
                invoice_id=updated_invoice['data'].id
            )
            background_tasks.add_task(orchestrator.startWorkflow, command)
        
        return updated_invoice
    
    
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
    response_model=BaseResponseSchema[InvoiceResponseSchema],
    status_code=201)
    @inject
    async def bulk(
        status: str,
        ids: list[str],
        background_tasks: BackgroundTasks,
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.updateInvoiceUsecase]
        ),
        orchestrator: WorkflowLauncher = Depends(
            Provide[AppContainer.orchestrator_container.localWorkflowLauncher]
        )
        
    ):
        invoices = []
        for id in ids:
            invoices.append(
                await useCase.execute(
                    InvoiceUpdateSchema(id=id, status=status)))

        if status == EnumInvoiceStatus.VALIDATED.value:
            for invoice in invoices:
                command = SyncUpdateInvoiceToPennylaneCommand(
                    workflow_id='INTERNAL',
                    workflow_name="updateInvoiceToPennylaneWorkflow",
                    invoice_id=invoice.get('data').id
                )
                background_tasks.add_task(orchestrator.startWorkflow, command)
                
        return BaseResponseSchema.response(
            message="Invoice bulk updated",
            status_code=201,
            data=[]
        )
    
    return router