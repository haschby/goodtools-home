import asyncio

from fastapi import APIRouter, Depends, Body
from pydantic import BaseModel
from application.containers.appContainer import AppContainer
from domain.models.goodtool import RentabilityBooking, Asset
from infrastructure.mappers.rentabilityItemMapper import build_rentability_items

from dependency_injector.wiring import inject, Provide


class BookingCommentUpdate(BaseModel):
    comment: str
    
    
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
        
        rentability, invoices = await asyncio.gather(
            gc_gateway.getRentabilitiesByBookingId(bookingId),
            invoice_repository.get_by_external_ids([bookingId]),
        )
        
        total_invoice = float(sum(row.amount_ht or 0 for row in invoices))
        total_rentability = float(sum(row["totalPriceHT"] or 0 for row in rentability))
            
        profit = total_invoice - total_rentability
        marging = profit / total_invoice if total_invoice else 0
        
        items = build_rentability_items(rentability, invoices)
        
        return {
            "data": {
                "comment": booking.comment,
                "bookingId": booking.bookingId,
                "isMonthly": booking.isMonthly,
                "isExternal": booking.isExternal,
                "isManualInvoice": booking.isManualInvoice,
                "items": items,
                "profit": profit or None,
                "charges": total_rentability or None,
                "ca": total_invoice or None,
                "margin": marging or None
            },
            "status_code": 200,
            "message": "Rentabilities fetched successfully"
        }

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

    # @router.post("/asset")
    # @inject
    # async def create_asset(
    #     asset: any,
    #     gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    # ):
    #     return await gc_gateway.createAsset(asset)
    
    return router