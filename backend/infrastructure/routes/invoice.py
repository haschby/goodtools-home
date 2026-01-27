from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from application.containers.appContainer import AppContainer
from application.usecases.baseUsecase import BaseUsecase
from domain.models.invoice import EnumInvoiceStatus

from application.dtos.baseDto import BaseResponseSchema
from application.dtos.invoiceDto import ( 
    InvoiceResponseSchema, 
    InvoiceCreateSchema, 
    InvoiceUpdateSchema
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
    status_code=201 )
    @inject
    async def count(
        repository: any = Depends(
            Provide[AppContainer.invoice_container.repository]
        )
    ):
        return await repository.count()
    
    @router.get(
    '/all',
    response_model=BaseResponseSchema[InvoiceResponseSchema],
    status_code=201)
    @inject
    async def invoices(
        status: Optional[str] = Query(default="All", description="Filter invoices by status"),
        cursor: Optional[str|None] = Query(default=None, description="Cursor Selector"),
        id: Optional[str|None] = Query(default=None, description="ID Selector"),
        getAllInvoicesUsecase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.getAllInvoicesUsecase]
        )
    ):
        params = {
            "status": status,
            "cursor": {
                "created_at": cursor,
                "id": id
            }
        }
        return await getAllInvoicesUsecase.execute(params)

    @router.post(
    '/',
    response_model=BaseResponseSchema[InvoiceResponseSchema],
    status_code=201)
    @inject
    async def create(
        new_invoice: InvoiceCreateSchema,
        createInvoiceUsecase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.createInvoiceUsecase]
        )
    ):
        return await createInvoiceUsecase.execute([new_invoice])
    
    @router.get(
    '/{id}',
    response_model=BaseResponseSchema[InvoiceResponseSchema],
    status_code=201)
    @inject
    async def invoice(
        id: str,
        getInvoiceUsecase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.getInvoiceUsecase]
        )
    ):
        return await getInvoiceUsecase.execute(id)
    
    @router.patch(
    '/{id}',
    response_model=BaseResponseSchema[InvoiceResponseSchema],
    status_code=201)
    @inject
    async def update(
        id: str,
        update_invoice: InvoiceUpdateSchema,
        updateInvoiceUsecase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.updateInvoiceUsecase]
        )
    ):
        update_invoice.id = id
        return await updateInvoiceUsecase.execute(update_invoice) 
    
    
    @router.post(
    '/search',
    response_model=BaseResponseSchema[InvoiceResponseSchema],
    status_code=201)
    async def search(
        query: str
    ):
        print('@QUERY', query)
        return { "message": "Search query", "status_code": 201, "data": [] }
    
    return router