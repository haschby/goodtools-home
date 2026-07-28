from application.dtos.buybackDto import (
    BuybackDetailSchema,
    BuybackDocumentSchema,
    BuybackDetailResponseSchema,
)
from application.ports.baseUsecase import BaseUsecase
from application.ports.StorageGateway import StorageFileGateway
from domain.services.buybackService import BuybackService


class GetBuybackById(BaseUsecase):
    """Use case: retrieve a single buyback and enrich it with a Pre-signed URL.

    It orchestrates two outbound ports and depends on neither HTTP, the ORM,
    nor the concrete storage provider (S3, Azure Blob, MinIO...):

    * the domain service (backed by the repository port) resolves the buyback;
    * the storage port generates a Pre-signed URL for the associated resource.

    The Pre-signed URL is a read-time concern and is never persisted on the
    domain entity.
    """

    def __init__(
        self,
        buybackService: BuybackService,
        storage: StorageFileGateway,
    ) -> None:
        self.buybackService = buybackService
        self.storage = storage

    async def execute(self, buyback_id: str) -> BuybackDetailResponseSchema:
        try:
            buyback = await self.buybackService.get_buyback_by_id(buyback_id)
        except Exception as error:  # noqa: BLE001 - surfaced as a 500 payload
            return BuybackDetailResponseSchema(
                message=f"Buyback not fetched: {error}",
                status_code=500,
                data=None,
            )

        if buyback is None:
            return BuybackDetailResponseSchema(
                message="Buyback not found",
                status_code=404,
                data=None,
            )

        detail = BuybackDetailSchema.model_validate(
            buyback, from_attributes=True
        )

        storage_key = buyback.file_path
        if storage_key:
            try:
                url = await self.storage.presigned_url(storage_key)
            except Exception as error:  # noqa: BLE001 - storage unavailable
                return BuybackDetailResponseSchema(
                    message=f"Presigned URL generation failed: {error}",
                    status_code=500,
                    data=None,
                )
            detail.document = BuybackDocumentSchema(
                storage_key=storage_key,
                url=url,
            )

        return BuybackDetailResponseSchema(
            message="Buyback fetched successfully",
            status_code=200,
            data=detail,
        )
