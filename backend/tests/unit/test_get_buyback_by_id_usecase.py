from datetime import datetime

import pytest

from application.usecases.buyback.getBuybackById import GetBuybackById
from domain.models.buyback import Buyback
from domain.services.buybackService import BuybackService


class FakeBuybackRepository:
    """In-memory fake implementing the BuybackRepositoryPort contract."""

    def __init__(self, stored=None):
        self.stored: list[Buyback] = list(stored or [])

    async def save_all(self, buybacks):
        self.stored.extend(buybacks)
        return buybacks

    async def find_by_ids(self, ids):
        return [b for b in self.stored if b.id in ids]

    async def find_all(self):
        return list(self.stored)

    async def find_by_id(self, buyback_id):
        return next((b for b in self.stored if b.id == buyback_id), None)


class ExplodingRepository(FakeBuybackRepository):
    async def find_by_id(self, buyback_id):
        raise RuntimeError("db is down")


class FakeStorage:
    """Records presigned_url calls and returns a deterministic URL."""

    def __init__(self):
        self.calls: list[tuple] = []

    async def presigned_url(self, file_name, expires_in=3600):
        self.calls.append((file_name, expires_in))
        return f"https://storage.test/{file_name}?sig=abc"


class ExplodingStorage(FakeStorage):
    async def presigned_url(self, file_name, expires_in=3600):
        raise RuntimeError("storage unavailable")


def _buyback(index: int, file_path: str | None = None) -> Buyback:
    return Buyback(
        id=f"BB{index}",
        amount=100 + index,
        status="to_be_traited",
        gc_booking=f"B-{index}",
        file_path=file_path,
        created_at=datetime(2026, 7, 8, 10, index),
        updated_at=datetime(2026, 7, 8, 10, index),
    )


def _usecase(repository, storage=None) -> GetBuybackById:
    return GetBuybackById(
        BuybackService(buybackRepository=repository),
        storage or FakeStorage(),
    )


@pytest.mark.asyncio
async def test_found_without_document_does_not_call_storage():
    repository = FakeBuybackRepository([_buyback(0, file_path=None)])
    storage = FakeStorage()
    usecase = _usecase(repository, storage)

    result = await usecase.execute("BB0")

    assert result.status_code == 200
    assert result.data is not None
    assert result.data.id == "BB0"
    assert result.data.document is None
    assert storage.calls == []


@pytest.mark.asyncio
async def test_found_with_document_generates_presigned_url():
    key = "buybacks/BB1/document.pdf"
    repository = FakeBuybackRepository([_buyback(1, file_path=key)])
    storage = FakeStorage()
    usecase = _usecase(repository, storage)

    result = await usecase.execute("BB1")

    assert result.status_code == 200
    assert result.data is not None
    assert result.data.document is not None
    assert result.data.document.storage_key == key
    assert result.data.document.url == f"https://storage.test/{key}?sig=abc"
    assert storage.calls == [(key, 3600)]


@pytest.mark.asyncio
async def test_not_found_returns_404():
    repository = FakeBuybackRepository([])
    storage = FakeStorage()
    usecase = _usecase(repository, storage)

    result = await usecase.execute("missing")

    assert result.status_code == 404
    assert result.data is None
    assert storage.calls == []


@pytest.mark.asyncio
async def test_repository_error_is_surfaced_as_500():
    usecase = _usecase(ExplodingRepository())

    result = await usecase.execute("BB0")

    assert result.status_code == 500
    assert result.data is None


@pytest.mark.asyncio
async def test_storage_error_is_surfaced_as_500():
    key = "buybacks/BB2/document.pdf"
    repository = FakeBuybackRepository([_buyback(2, file_path=key)])
    usecase = _usecase(repository, ExplodingStorage())

    result = await usecase.execute("BB2")

    assert result.status_code == 500
    assert result.data is None
