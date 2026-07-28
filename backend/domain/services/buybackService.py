from typing import List, Optional, Tuple, Dict

from application.dtos.buybackDto import BuybackCreateSchema, BuybackPatchSchema
from application.ports.buybackRepository import BuybackRepositoryPort
from domain.buyback.buybackFactory import BuybackFactory
from domain.models.buyback import Buyback

class BuybackService:
    """Domain service orchestrating buyback business operations.

    It depends only on the repository port, never on the concrete adapter.
    """

    def __init__(self, buybackRepository: BuybackRepositoryPort) -> None:
        self.repository = buybackRepository

    async def create_buybacks(
        self, buybacks: List[BuybackCreateSchema]
    ) -> List[Buyback]:
        entities = BuybackFactory.create_many(
            [
                {
                    "amount": buyback.amount,
                    "currency": buyback.currency,
                    "gc_booking": buyback.gc_booking,
                    "status": buyback.status,
                    "file_path": buyback.file_path,
                }
                for buyback in buybacks
            ]
        )

        created = await self.repository.save_all(entities)

        # Reload from the source of truth so the caller receives the
        # authoritative, DB-refreshed representation.
        return await self.repository.find_by_ids(
            [buyback.id for buyback in created]
        )

    async def get_all_buybacks(self, params: Optional[dict] = None) -> Tuple[List[Buyback], List[dict], int]:
        """Return every buyback as domain entities.

        No business rule currently constrains the listing, but this is the
        seam where sorting/filtering invariants would live.
        """
        items, count_by_status, count = await self.repository.get_all(
            status=params['status'],
            page=params['page'],
            limit=params['limit'],
            query=params['query']
        )
        return items, count_by_status, count

    async def get_buyback_by_id(self, buyback_id: str) -> Optional[Buyback]:
        """Return a single buyback by id, or ``None`` when it does not exist."""
        return await self.repository.find_by_id(buyback_id)
    
    async def patch(self, buyback: BuybackPatchSchema) -> Buyback:
        """Patch a buyback"""
        return await self.repository.patch(buyback)
