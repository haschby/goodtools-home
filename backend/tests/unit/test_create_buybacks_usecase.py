from datetime import datetime

import pytest

from application.dtos.buybackDto import BuybackCreateSchema
from application.usecases.buyback.createBuybacks import CreateBuybacks
from domain.buyback.buybackFactory import BuybackValidationError
from domain.models.buyback import Buyback
from domain.services.buybackService import BuybackService


class FakeBuybackRepository:
    """In-memory fake implementing the BuybackRepositoryPort contract."""

    def __init__(self):
        self.saved: list[Buyback] = []
        self.save_all_calls = 0
        self.find_by_ids_calls: list[list[str]] = []

    async def save_all(self, buybacks):
        self.save_all_calls += 1
        for index, buyback in enumerate(buybacks):
            buyback.id = f"BB{index}"
            buyback.created_at = datetime(2026, 7, 8, 10, index)
            buyback.updated_at = datetime(2026, 7, 8, 10, index)
        self.saved = list(buybacks)
        return buybacks

    async def find_by_ids(self, ids):
        self.find_by_ids_calls.append(ids)
        return [b for b in self.saved if b.id in ids]


class ExplodingRepository(FakeBuybackRepository):
    async def save_all(self, buybacks):
        raise RuntimeError("db is down")


def _usecase(repository):
    return CreateBuybacks(BuybackService(buybackRepository=repository))


@pytest.mark.asyncio
async def test_creates_list_of_buybacks_and_returns_refreshed():
    repository = FakeBuybackRepository()
    usecase = _usecase(repository)

    payload = [
        BuybackCreateSchema(gc_booking="B-123", amount=100, currency="EUR"),
        BuybackCreateSchema(gc_booking="B-456", amount=200, currency="EUR"),
    ]

    result = await usecase.execute(payload)

    assert result.status_code == 201
    assert result.data is not None
    assert len(result.data) == 2
    assert {b.amount for b in result.data} == {100, 200}


@pytest.mark.asyncio
async def test_repository_is_called_correctly():
    repository = FakeBuybackRepository()
    usecase = _usecase(repository)

    await usecase.execute(
        [BuybackCreateSchema(amount=100, currency="EUR")]
    )

    assert repository.save_all_calls == 1
    # find_by_ids reloads from source of truth using the created ids
    assert repository.find_by_ids_calls == [["BB0"]]


@pytest.mark.asyncio
async def test_returns_data_refreshed_from_repository():
    repository = FakeBuybackRepository()
    usecase = _usecase(repository)

    result = await usecase.execute(
        [BuybackCreateSchema(amount=50, currency="EUR")]
    )

    assert result.data[0].id == "BB0"
    assert result.data[0].created_at is not None


@pytest.mark.asyncio
async def test_empty_list_returns_business_error():
    repository = FakeBuybackRepository()
    usecase = _usecase(repository)

    result = await usecase.execute([])

    assert result.status_code == 422
    assert result.data is None
    assert repository.save_all_calls == 0


@pytest.mark.asyncio
async def test_business_error_is_propagated_as_422():
    class RejectingService(BuybackService):
        async def create_buybacks(self, buybacks):
            raise BuybackValidationError("amount must be strictly positive")

    usecase = CreateBuybacks(RejectingService(FakeBuybackRepository()))

    result = await usecase.execute(
        [BuybackCreateSchema(amount=10, currency="EUR")]
    )

    assert result.status_code == 422
    assert "Business rule violation" in result.message


@pytest.mark.asyncio
async def test_db_error_is_propagated_as_500():
    usecase = _usecase(ExplodingRepository())

    result = await usecase.execute(
        [BuybackCreateSchema(amount=10, currency="EUR")]
    )

    assert result.status_code == 500
    assert result.data is None


def test_invalid_currency_rejected_at_dto_level():
    with pytest.raises(ValueError):
        BuybackCreateSchema(amount=10, currency="JPY")


def test_negative_amount_rejected_at_dto_level():
    with pytest.raises(ValueError):
        BuybackCreateSchema(amount=-5, currency="EUR")
