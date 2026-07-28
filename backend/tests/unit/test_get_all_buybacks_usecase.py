from datetime import datetime

import pytest

from application.usecases.buyback.getAllBuybacks import GetAllBuybacks
from domain.models.buyback import Buyback
from domain.services.buybackService import BuybackService


class FakeBuybackRepository:
    """In-memory fake implementing the BuybackRepositoryPort contract."""

    def __init__(self, stored=None):
        self.stored: list[Buyback] = list(stored or [])
        self.find_all_calls = 0

    async def save_all(self, buybacks):
        self.stored.extend(buybacks)
        return buybacks

    async def find_by_ids(self, ids):
        return [b for b in self.stored if b.id in ids]

    async def find_all(self):
        self.find_all_calls += 1
        return list(self.stored)


class ExplodingRepository(FakeBuybackRepository):
    async def find_all(self):
        raise RuntimeError("db is down")


def _buyback(index: int) -> Buyback:
    return Buyback(
        id=f"BB{index}",
        amount=100 + index,
        status="to_be_traited",
        gc_booking=f"B-{index}",
        created_at=datetime(2026, 7, 8, 10, index),
        updated_at=datetime(2026, 7, 8, 10, index),
    )


def _usecase(repository) -> GetAllBuybacks:
    return GetAllBuybacks(BuybackService(buybackRepository=repository))


@pytest.mark.asyncio
async def test_returns_list_of_buybacks():
    repository = FakeBuybackRepository([_buyback(0), _buyback(1)])
    usecase = _usecase(repository)

    result = await usecase.execute()

    assert result.status_code == 201
    assert result.data is not None
    assert result.data.total == 2
    assert result.data.page == 1
    assert result.data.total_pages == 1
    assert len(result.data.items) == 2
    assert {b.id for b in result.data.items} == {"BB0", "BB1"}


@pytest.mark.asyncio
async def test_repository_find_all_is_called():
    repository = FakeBuybackRepository([_buyback(0)])
    usecase = _usecase(repository)

    await usecase.execute()

    assert repository.find_all_calls == 1


@pytest.mark.asyncio
async def test_empty_repository_returns_empty_paginated_payload():
    repository = FakeBuybackRepository([])
    usecase = _usecase(repository)

    result = await usecase.execute()

    assert result.status_code == 201
    assert result.data is not None
    assert result.data.items == []
    assert result.data.total == 0


@pytest.mark.asyncio
async def test_repository_error_is_propagated_as_500():
    usecase = _usecase(ExplodingRepository())

    result = await usecase.execute()

    assert result.status_code == 500
    assert result.data is None
    assert "not fetched" in result.message
