from domain.models.invoice import Invoice, EnumInvoiceStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_, and_
from typing import Optional
from .baseRepository import BaseRepository
from datetime import datetime

class InvoiceRepositoryImpl(BaseRepository[Invoice]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Invoice)
    
    async def get_all(
        self,
        status: Optional[str] = "All",
        cursor: Optional[str] = None,
        limit: Optional[int] = 30
    ) -> list[Invoice]:
        command = select(Invoice)
        
        print('@=>>> cursor', cursor)
        print('@=>>> status', status)
        print('@=>>> limit', limit)

        if status and status != "All":
            command = command.where(Invoice.status == status)            
        
        if cursor and cursor["id"] and cursor["created_at"]:
            command = command.where(
                or_(
                    Invoice.created_at < datetime.fromisoformat(cursor["created_at"]),
                    and_(
                        Invoice.created_at == datetime.fromisoformat(cursor["created_at"]),
                        Invoice.id < str(cursor["id"])
                    )
                )
            )

        command = command.order_by(desc(Invoice.created_at), desc(Invoice.id))
        result = await self._session.execute(command.limit(limit))
        return result.scalars().all()

    async def get_by_id(self, id: str) -> Invoice:
        result = await self._session.execute(
            select(Invoice).where(Invoice.id == id)
        )
        return result.scalar_one_or_none()

    async def update(self, invoice: Invoice) -> Invoice:
        self._session.add(invoice)
        await self._session.commit()
        await self._session.refresh(invoice)
        return invoice