from abc import ABC, abstractmethod
from typing import List, Optional
from domain.models.buyback import Buyback


class BuybackRepositoryPort(ABC):
    """Outbound port for buyback persistence.

    The application layer depends only on this abstraction and never on the
    concrete ORM / SQL implementation.
    """

    @abstractmethod
    async def save_all(self, buybacks: List[Buyback]) -> List[Buyback]:
        """Persist a list of buybacks atomically and return them."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_ids(self, ids: List[str]) -> List[Buyback]:
        """Reload the persisted buybacks from the source of truth."""
        raise NotImplementedError

    @abstractmethod
    async def find_by_id(self, buyback_id: str) -> Optional[Buyback]:
        """Return a single buyback by its identifier, or ``None`` if absent."""
        raise NotImplementedError

    @abstractmethod
    async def find_all(self) -> List[Buyback]:
        """Return every persisted buyback.

        The signature is intentionally simple for this first version; it is
        expected to evolve towards ``find_all(filters, pagination)`` as sorting,
        filtering and pagination requirements emerge.
        """
        raise NotImplementedError
