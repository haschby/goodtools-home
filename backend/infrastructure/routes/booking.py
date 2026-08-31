from fastapi import APIRouter, Depends, Body
from application.containers.appContainer import AppContainer
from domain.models.goodtool import RentabilityBooking, Asset

from dependency_injector.wiring import inject, Provide
    
    
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
        gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    ):
        rows = await gc_gateway.getRentabilitiesByBookingId(bookingId)
        print("rows => ", rows) 
        if not rows:
            return {
                "data": [],
                "status_code": 200,
                "message": "No rentabilities found"
            }
        
        bookings = []
        payloads = []
        external = False
        isMonthly = False
        manualInvoice = False
        bookingId = None
        
        for row in rows:
            if row.type == "ProviderPrice":
                payloads.append(row)
            elif row.type == "GoodcollectPrice":
                bookings.append(row)
            
            isMonthly = row.isMonthly
            manualInvoice = row.isManualInvoice
            external = row.isExternal
            bookingId = row.bookingId
            
        
        total_payload = sum(row.totalPriceHT for row in bookings)
        total_provider = sum(row.totalPriceHT for row in payloads)
        profit = total_payload - total_provider
        marging = (profit / total_provider) * 100 if total_provider else 0
        
        return {
            "data": {
                "bookingId": row.bookingId,
                "isMonthly": isMonthly,
                "isExternal": external,
                "isManualInvoice": manualInvoice,
                "items": list(bookings) + list(payloads),
                "profit": profit,
                "charges": total_provider,
                "ca": total_payload,
                "margin": marging
            },
            "status_code": 200,
            "message": "Rentabilities fetched successfully"
        }

    # @router.post("/asset")
    # @inject
    # async def create_asset(
    #     asset: any,
    #     gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    # ):
    #     return await gc_gateway.createAsset(asset)
    
    return router