from typing import List

from application.dtos.buybackDto import (
    BuybackCreateSchema,
    BuybackResponseSchema,
    BuybackListResponseSchema,
)
from application.ports.baseUsecase import BaseUsecase
from domain.buyback.buybackFactory import BuybackValidationError
from domain.services.invoiceService import InvoiceService
from domain.models.enums import EnumInvoiceType, EnumInvoiceStatus
from application.dtos.invoiceDto import InvoiceResponseSchema
from application.dtos.invoiceDto import InvoiceCreateSchema

class CreateBuybacks(BaseUsecase):
    """Use case: create a list of buybacks and return them refreshed from DB.

    Depends only on the domain service (which itself depends on the repository
    port). It knows nothing about HTTP, the ORM model, or SQL.
    """

    def __init__(self, invoiceService: InvoiceService) -> None:
        self.invoiceService = invoiceService

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
            invoices = [
                InvoiceCreateSchema(
                    name=buyback.file_path,
                    path=buyback.file_path,
                    invoice_type=EnumInvoiceType.BUYBACK,
                    file_path=buyback.file_path,
                    status=EnumInvoiceStatus.TO_BE_TRAITED,
                    amount=buyback.amount,
                    currency=buyback.currency,
                )
                for buyback in buybacks
            ]
            created = await self.invoiceService.create_invoice(invoices)
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
                InvoiceResponseSchema.model_validate(invoice, from_attributes=True)
                for invoice in created
            ],
        )
