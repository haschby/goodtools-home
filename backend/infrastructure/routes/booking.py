import asyncio

from fastapi import APIRouter, Depends, Body, BackgroundTasks
from pydantic import BaseModel
from application.containers.appContainer import AppContainer
from application.ports.baseUsecase import BaseUsecase
from application.ports.orchestrator.workflowLauncher import WorkflowLauncher
from application.dtos.workflow import SyncInvoiceToGcCommand
from domain.models.goodtool import RentabilityBooking, Asset
from infrastructure.mappers.rentabilityItemMapper import build_rentability_items

from dependency_injector.wiring import inject, Provide


class BookingCommentUpdate(BaseModel):
    comment: str


class BookingRentabilityCreate(BaseModel):
    invoiceId: str
    
    
def booking_routes() -> APIRouter:
    
    router = APIRouter(
        prefix="/client/gc/booking",
        tags=["gc_booking"]
    )
    
    @router.get("/{id:int}")
    @inject
    async def get_booking(
        id: int,
        gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    ):
        return await gc_gateway.getRentabilityBooking(id)
    
    
    @router.post("/asset")
    @inject
    async def create_asset(
        asset: Asset = Body(...),
        gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    ):
        return await gc_gateway.createAsset(asset)
    
    @router.post("/rentability-booking")
    @inject
    async def create_rentability_booking(
        rentability_booking: RentabilityBooking = Body(...),
        gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    ):
        return await gc_gateway.createRentabilityBooking(rentability_booking)
    
    @router.get("/{bookingId:int}/rentabilities")
    @inject
    async def get_rentabilities_booking(
        bookingId: int,
        gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway]),
        invoice_repository: any = Depends(Provide[AppContainer.invoice_container.repository])
    ):
        booking = await gc_gateway.getBookingById(bookingId)
        if not booking:
            return {
                "data": [],
                "status_code": 200,
                "message": "No booking found"
            }
        
        rentabilities, invoices = await asyncio.gather(
            gc_gateway.getRentabilitiesByBookingId(bookingId),
            invoice_repository.get_by_gc_booking(bookingId),
        )
        
        total_invoice = float(sum(row.amount_ht or 0 for row in invoices))
        total_rentability = float(sum(row["totalPriceHT"] or 0 for row in rentabilities))
            
        profit = total_rentability - total_invoice 
        marging = profit / total_invoice if total_invoice else 0
        
        items = build_rentability_items(rentabilities, invoices)
        
        return {
            "data": {
                "comment": booking.comment,
                "isClosed": booking.isClosed,
                "bookingId": booking.bookingId,
                "eventStartDate": booking.bookingStartDate,
                "eventEndDate": booking.bookingEndDate,
                "isMonthly": booking.isMonthly,
                "isExternal": booking.isExternal,
                "isManualInvoice": booking.isManualInvoice,
                "items": items,
                "profit": profit or None,
                "ca": total_rentability or None,
                "charges": total_invoice or None,
                "margin": marging * 100 or None
            },
            "status_code": 200,
            "message": "Rentabilities fetched successfully"
        }

    @router.post("/{bookingId:int}/rentabilities")
    @inject
    async def create_booking_rentability(
        bookingId: int,
        background_tasks: BackgroundTasks,
        payload: BookingRentabilityCreate = Body(...),
        gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway]),
        useCase: BaseUsecase = Depends(
            Provide[AppContainer.invoice_container.importInvoiceToBookingUsecase]
        ),
        orchestrator: WorkflowLauncher = Depends(
            Provide[AppContainer.orchestrator_container.localWorkflowLauncher]
        )
    ):
        try:
            booking = await gc_gateway.getBookingById(bookingId)
        except Exception as e:
            return {
                "data": None,
                "status_code": 500,
                "message": f"Failed to fetch booking: {str(e)}"
            }

        if not booking:
            return {
                "data": None,
                "status_code": 404,
                "message": "No booking found"
            }

        try:
            response = await useCase.execute(bookingId, payload.invoiceId)
        except Exception as e:
            return {
                "data": None,
                "status_code": 500,
                "message": f"Failed to import invoice: {str(e)}"
            }

        # Mirror the invoice on the GC booking (Asset + BookingRentabilityLine)
        # with the existing workflow, as done when a gc_booking is added.
        if getattr(useCase, "gc_sync_needed", False) and useCase.invoice_id:
            gc_command = SyncInvoiceToGcCommand(
                workflow_id='INTERNAL-SYNC-GOOD-COLLECT',
                workflow_name="syncInvoiceToGcWorkflow",
                invoice_id=useCase.invoice_id
            )
            background_tasks.add_task(orchestrator.startWorkflow, gc_command)

        return response

    @router.patch("/{bookingId:int}/comment")
    @inject
    async def update_booking_comment(
        bookingId: int,
        payload: BookingCommentUpdate = Body(...),
        gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    ):
        updated = await gc_gateway.updateBookingComment(bookingId, payload.comment)
        if not updated:
            return {
                "data": None,
                "status_code": 404,
                "message": "No booking found"
            }
        return {
            "data": updated,
            "status_code": 200,
            "message": "Booking comment updated successfully"
        }

    @router.patch("/{bookingId:int}/status/close")
    @inject
    async def close_booking(
        bookingId: int,
        gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    ):
        closed = await gc_gateway.closeBookingRentability(bookingId)
        if not closed:
            return {
                "data": None,
                "status_code": 404,
                "message": "No booking found"
            }
        return {
            "data": closed,
            "status_code": 200,
            "message": "Booking closed successfully"
        }

    # @router.post("/asset")
    # @inject
    # async def create_asset(
    #     asset: any,
    #     gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    # ):
    #     return await gc_gateway.createAsset(asset)
    
    return router