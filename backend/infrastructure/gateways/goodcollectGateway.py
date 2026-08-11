from logging import Logger
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, text
from typing import Any

from domain.models.goodtool import RentabilityBooking, Asset


class GoodcollectGateway:
    
    def __init__(self, session: async_sessionmaker, logger: Logger):
        self.session = session
        self.logger = logger
        
    async def getBooking(self, id: int) -> Any:
        async with self.session() as session:
            stmt = text('SELECT id FROM "Booking" WHERE id = :id LIMIT 10')
            test = await session.execute(stmt, {"id": id})                
            return test.scalars().all()
    
    async def getRentabilityBooking(self, id: int) -> Any:
        async with self.session() as session:
            stmt = text('SELECT id FROM "BookingRentabilityLine" WHERE "bookingId" = :id OR "comment" = :id')
            test = await session.execute(stmt, {"id": id, "comment": id})
            return test.scalars().all()

    async def findRentabilityLineById(self, line_id: str) -> Any:
        """Return the rentability line by its own id.

        Used when the invoice carries a stored `crm_id` mapping to the GC
        rentability line, so the line can be located even if its `bookingId`
        (gc_booking) has since changed. Returns None when nothing matches.
        """
        async with self.session() as session:
            stmt = text(
                'SELECT "id", "priceHT", "bookingId", "assetId", "type", "comment" '
                'FROM "BookingRentabilityLine" '
                'WHERE "id" = :line_id '
                'LIMIT 1'
            )
            result = await session.execute(stmt, {"line_id": str(line_id)})
            row = result.mappings().first()
            return dict(row) if row else None

    async def findRentabilityLineByComment(self, comment: str) -> Any:
        """Return the existing rentability line matching an invoice.

        Matches on the free-text comment, which stores the originating
        invoice id. Returns the full row so the caller can decide whether to
        update it, or None when nothing exists.
        """
        async with self.session() as session:
            stmt = text(
                'SELECT "id", "priceHT", "bookingId", "assetId", "type", "comment" '
                'FROM "BookingRentabilityLine" '
                'WHERE "comment" = :comment '
                'LIMIT 1'
            )
            result = await session.execute(stmt, {"comment": str(comment)})
            row = result.mappings().first()
            return dict(row) if row else None
    
    async def createAsset(self, payload: Asset) -> Any:
        async with self.session() as session:
            params = {
                "id": str(uuid.uuid4()),
                "fileKey": payload.fileKey,
                "fileUrl": payload.fileUrl,
            }
            stmt = text(
                'INSERT INTO "Asset" ("id", "fileKey", "fileUrl") '
                'VALUES (:id, :fileKey, :fileUrl) '
                'RETURNING "id"'
            )
            try:
                result = await session.execute(stmt, params)
                await session.commit()
                return result.mappings().one()
            except Exception as e:
                print("CREATE_ASSET error", e)
                raise Exception(e)
    
    async def createRentabilityBooking(self, payload: RentabilityBooking) -> Any:
        async with self.session() as session:
            params = {
                "id": str(uuid.uuid4()),
                "dateUpdated": payload.dateUpdated or datetime.utcnow(),
                "bookingId": payload.bookingId,
                "assetId": payload.assetId,
                "priceHT": payload.priceHT,
                "comment": payload.comment,
            }
            stmt = text(
                'INSERT INTO "BookingRentabilityLine" ("id", "dateUpdated", "priceHT", "bookingId", "assetId", "comment") '
                'VALUES (:id, :dateUpdated, :priceHT, :bookingId, :assetId, :comment) '
                'RETURNING "id", "priceHT", "bookingId", "assetId", "comment"'
            )
            result = await session.execute(stmt, params)
            await session.commit()
            return result.mappings().one()

    async def updateRentabilityBooking(self, line_id: str, payload: RentabilityBooking) -> Any:
        """Update an existing rentability line, only for the filled-out fields.

        `priceHT` (amount), `bookingId` (gc_booking) and `type` (status) are
        applied only when provided on the payload, so untouched fields are left
        as-is. `dateUpdated` is always refreshed.
        """
        updates = {"dateUpdated": payload.dateUpdated or datetime.utcnow()}
        if payload.priceHT is not None:
            updates["priceHT"] = payload.priceHT
        if payload.bookingId is not None:
            updates["bookingId"] = payload.bookingId
        if getattr(payload, "type", None) is not None:
            updates["type"] = payload.type

        set_clause = ", ".join(f'"{column}" = :{column}' for column in updates)
        async with self.session() as session:
            stmt = text(
                f'UPDATE "BookingRentabilityLine" SET {set_clause} '
                'WHERE "id" = :line_id '
                'RETURNING "id", "priceHT", "bookingId", "assetId", "type", "comment"'
            )
            result = await session.execute(stmt, {**updates, "line_id": line_id})
            await session.commit()
            return result.mappings().one()
    
    async def getRentabilitiesByBookingId(self, bookingId: int) -> Any:
        async with self.session() as session:
            stmt = text('SELECT "id", "priceHT", "bookingId", "assetId", "type", SUM("priceHT") AS "totalPriceHT" FROM "BookingRentabilityLine" WHERE "bookingId" = :bookingId GROUP BY "id", "priceHT", "bookingId", "assetId", "type"')
            rows = await session.execute(stmt, {"bookingId": bookingId})
            return rows.mappings().all()
            