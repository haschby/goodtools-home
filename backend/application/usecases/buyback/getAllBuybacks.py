from application.dtos.buybackDto import (
    BuybackResponseSchema,
    PaginatedBuybackResponseSchema,
    BuybackPaginatedListResponseSchema,
)
from application.ports.baseUsecase import BaseUsecase
from domain.services.buybackService import BuybackService
import math
from typing import Optional

class GetAllBuybacks(BaseUsecase):
    """Use case: retrieve every buyback.

    Depends only on the domain service (which itself depends on the repository
    port). It knows nothing about HTTP, the ORM model, or SQL. An empty
    database is a valid outcome and is returned as an empty paginated payload.

    The result is wrapped in a paginated envelope (single page for now) so the
    contract already matches the shared data-table pagination shape and can
    evolve towards real server-side pagination without breaking clients.
    """

    def __init__(self, buybackService: BuybackService) -> None:
        self.buybackService = buybackService

    async def execute(self, params: Optional[dict] = None) -> BuybackPaginatedListResponseSchema:
        
        buybacks, _, count = await self.buybackService.get_all_buybacks(params)
        
        items = [
            BuybackResponseSchema.model_validate(buyback, from_attributes=True)
            for buyback in buybacks
        ]
        
        total_by_status = {
            "TO_BE_TRAITED": len([buyback for buyback in buybacks if buyback.status == "A Traiter"]),
            "VALIDATED": len([buyback for buyback in buybacks if buyback.status == "Valider"]),
        }
        
        return BuybackPaginatedListResponseSchema(
            message="Buybacks fetched successfully",
            status_code=201,
            data=PaginatedBuybackResponseSchema(
                items=items,
                page=params.get('page', 1),
                limit=params.get('limit', 30),
                total=count,
                total_pages=math.ceil(count / params['limit']) if count else 1,
                total_by_status=total_by_status,
            ),
        )