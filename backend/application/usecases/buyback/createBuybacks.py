from typing import List

from application.dtos.buybackDto import (
    BuybackCreateSchema,
    BuybackResponseSchema,
    BuybackListResponseSchema,
)
from application.ports.baseUsecase import BaseUsecase
from domain.buyback.buybackFactory import BuybackValidationError
from domain.services.buybackService import BuybackService


class CreateBuybacks(BaseUsecase):
    """Use case: create a list of buybacks and return them refreshed from DB.

    Depends only on the domain service (which itself depends on the repository
    port). It knows nothing about HTTP, the ORM model, or SQL.
    """

    def __init__(self, buybackService: BuybackService) -> None:
        self.buybackService = buybackService

    async def execute(
        self, buybacks: List[BuybackCreateSchema]
    ) -> BuybackListResponseSchema:
        if not buybacks:
            return BuybackListResponseSchema(
                message="Buyback list must not be empty",
                status_code=422,
                data=None,
            )

        try:
            created = await self.buybackService.create_buybacks(buybacks)
        except BuybackValidationError as error:
            return BuybackListResponseSchema(
                message=f"Business rule violation: {error}",
                status_code=422,
                data=None,
            )
        except Exception as error:  # noqa: BLE001 - surfaced as a 500 payload
            return BuybackListResponseSchema(
                message=f"Buybacks not created: {error}",
                status_code=500,
                data=None,
            )

        return BuybackListResponseSchema(
            message="Buybacks created successfully",
            status_code=201,
            data=[
                BuybackResponseSchema.model_validate(buyback, from_attributes=True)
                for buyback in created
            ],
        )
