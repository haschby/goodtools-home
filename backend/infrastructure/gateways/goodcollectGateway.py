from logging import Logger
from datetime import datetime
import uuid
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select, text
from typing import Any

from domain.models.goodtool import RentabilityBooking, Asset


class CreateAssetError(Exception):
    pass


class CreateRentabilityLineError(Exception):
    pass


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
            stmt = text('SELECT id FROM "BookingRentabilityLine" WHERE "bookingId" = :id')
            test = await session.execute(stmt, {"id": id})
            return test.scalars().all()
    
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
            
            result = await session.execute(stmt, params)
            await session.commit()
            return result.mappings().one()
    
    async def createRentabilityBooking(self, payload: RentabilityBooking) -> Any:
        async with self.session() as session:
            params = {
                "id": str(uuid.uuid4()),
                "dateUpdated": payload.dateUpdated or datetime.utcnow(),
                "bookingId": payload.bookingId,
                "assetId": payload.assetId,
                "priceHT": payload.priceHT,
            }
            stmt = text(
                'INSERT INTO "BookingRentabilityLine" ("id", "dateUpdated", "priceHT", "bookingId", "assetId") '
                'VALUES (:id, :dateUpdated, :priceHT, :bookingId, :assetId) '
                'RETURNING "id", "priceHT", "bookingId", "assetId"'
            )
            result = await session.execute(stmt, params)
            await session.commit()
            return result.mappings().one()
    
    async def getRentabilitiesByBookingId(self, bookingId: int) -> Any:
        async with self.session() as session:
            stmt = text('SELECT "id", "priceHT", "bookingId", "assetId" FROM "BookingRentabilityLine" WHERE "bookingId" = :bookingId')
            rows = await session.execute(stmt, {"bookingId": bookingId})
            return rows.mappings().all()
            