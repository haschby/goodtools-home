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
        print(rows) 
        if not rows:
            return {
                "items": [],
                "net_profit": 0,
                "total_price": 0,
                "marging": 0
            }
        
        bookings = []
        payloads = []
        for row in rows:
            if row.type == "ProviderPrice":
                payloads.append(row)
            elif row.type == "GoodcollectPrice":
                bookings.append(row)
        
        total_payload = sum(row.totalPriceHT for row in bookings)
        total_provider = sum(row.totalPriceHT for row in payloads)
        profit = total_provider - total_payload
        marging = (profit / total_provider) * 100 if total_provider else 0
        
        print('@PROFIT', profit)
        print('@TOTAL_PROVIDER', total_provider)
        print('@TOTAL_PAYLOAD', total_payload)
        print('@MARGING', marging)
        
        
        return {
            "items": list(bookings) + list(payloads),
            "net_profit": profit,
            "total_price": total_payload,
            "marging": marging
        }

    # @router.post("/asset")
    # @inject
    # async def create_asset(
    #     asset: any,
    #     gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    # ):
    #     return await gc_gateway.createAsset(asset)
    
    return router