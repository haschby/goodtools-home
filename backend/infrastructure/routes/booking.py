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
        return await gc_gateway.getRentabilitiesByBookingId(bookingId)

    # @router.post("/asset")
    # @inject
    # async def create_asset(
    #     asset: any,
    #     gc_gateway: any = Depends(Provide[AppContainer.goodcollect_container.goodcollect_gateway])
    # ):
    #     return await gc_gateway.createAsset(asset)
    
    return router