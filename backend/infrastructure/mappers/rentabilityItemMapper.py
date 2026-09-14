from typing import Any, Callable, Iterable


def _get(source: Any, key: str, default: Any = None) -> Any:
    """Read a value from a dict-like row or an object (pydantic/ORM)."""
    if source is None:
        return default
    if isinstance(source, dict):
        return source.get(key, default)
    return getattr(source, key, default)


def map_rentability_item(
    *,
    id: Any = None,
    priceHT: Any = None,
    totalPriceHT: Any = None,
    bookingId: Any = None,
    assetId: Any = None,
    type: str | None = None,
    status: str | None = None
) -> dict:
    """Normalize a single line into the generic item shape expected by the frontend.

    Matches the `Rentability` interface:
    { id, priceHT, bookingId, assetId, type, totalPriceHT }
    """
    amount = totalPriceHT if totalPriceHT is not None else priceHT
    return {
        "id": str(id) if id is not None else None,
        "priceHT": priceHT if priceHT is not None else amount,
        "totalPriceHT": amount,
        "bookingId": str(bookingId) if bookingId is not None else None,
        "assetId": str(assetId) if assetId is not None else None,
        "type": type,
        "status": status,
    }


def map_rentability_line(line: Any) -> dict:
    """Map a GC `BookingRentabilityLine` row to the generic item shape."""
    return map_rentability_item(
        id=_get(line, "rentabilityLineId") or _get(line, "id"),
        totalPriceHT=_get(line, "totalPriceHT") or _get(line, "priceHT"),
        bookingId=_get(line, "bookingId"),
        assetId=_get(line, "assetId"),
        type=_get(line, "type")
    )


def map_invoice(invoice: Any) -> dict:
    """Map a supplier `Invoice` (dict row or model) to the generic item shape."""
    return map_rentability_item(
        id=_get(invoice, "id"),
        totalPriceHT=_get(invoice, "amount_ht"),
        bookingId=_get(invoice, "gc_booking") or _get(invoice, "external_id"),
        assetId=None,
        type=_get(invoice, "invoice_type") or "ProviderPrice",
        status=_get(invoice, "status"),
    )


def map_items(
    sources: Iterable[Any],
    mapper: Callable[[Any], dict],
) -> list[dict]:
    """Apply a mapper over a list of sources, skipping empty entries."""
    return [mapper(source) for source in sources or [] if source is not None]


def build_rentability_items(
    rentability_lines: Iterable[Any] | None,
    invoices: Iterable[Any] | None,
) -> list[dict]:
    """Merge GC rentability lines and supplier invoices into a single generic list."""
    return [
        *map_items(rentability_lines, map_rentability_line),
        *map_items(invoices, map_invoice),
    ]
