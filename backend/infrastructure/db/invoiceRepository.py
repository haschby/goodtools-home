from domain.models.invoice import Invoice, EnumInvoiceStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_, and_, text
from decimal import Decimal, InvalidOperation
from typing import Optional
from datetime import datetime
from .queries.invoices import (
    QUERY_GET_ALL_INVOICES,
    QUERY_GET_LAST_INVOICE_ID,
    QUERY_GET_INVOICE_BY_ID,
    QUERY_GET_INVOICE_ID
)

from .baseRepository import BaseRepository

class InvoiceRepositoryImpl(BaseRepository[Invoice]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Invoice)
    
    async def get_all(
        self,
        status: Optional[str] = "All",
        cursor: Optional[dict] = None,
        limit: Optional[int] = 30
    ) -> list[Invoice]:
        
        conditions = []
        params = {"limit": limit}

        # STATUS FILTER
        if status and status != "All":
            conditions.append("status = :status")
            params["status"] = status

        # CURSOR PAGINATION
        if cursor and cursor.get("created_at") and cursor.get("id"):
            cursor_created_at = datetime.fromisoformat(cursor["created_at"])
            conditions.append("(created_at, id) < (:cursor_created_at, :cursor_id)")
            params["cursor_created_at"] = cursor_created_at
            params["cursor_id"] = cursor["id"]

        # WHERE CLAUSE
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""

        query = f"""
        {QUERY_GET_ALL_INVOICES}
        {where_clause}
        ORDER BY created_at DESC, id DESC
        LIMIT :limit
        """
        
        async with self._session as session:
            result = await session.execute(text(query), params)
            invoices = result.mappings().all()
                
        return [Invoice(**row) for row in invoices] 

    async def get_by_id(
        self,
        id: str
    ) -> Invoice:
        
        stmt = select(Invoice).where(
            (Invoice.id == id) |
            (Invoice.external_id == id)
        )

        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    
    async def get_last_invoice_id(self) -> Optional[str]:
        async with self._session as session:
            result = await session.execute(text(QUERY_GET_LAST_INVOICE_ID))
            return result.scalar_one_or_none()

    async def get_by_external_ids(
        self,
        external_ids: list[str]
    ) -> list[Invoice]:
        query = f"""
        {QUERY_GET_INVOICE_BY_ID}
        WHERE external_id = ANY(:external_ids)
        """
        async with self._session as session:
            result = await session.execute(
                text(query),
                { "external_ids" : external_ids }
            )
            invoices = result.mappings().all()
            return [Invoice(**row) for row in invoices]
        
    
    async def search(self, q: str, limit: int = 30, offset: int = 0) -> list[Invoice]:
        sql = f"""
        {QUERY_GET_ALL_INVOICES}
        WHERE
            search_vector @@ plainto_tsquery(:q)
            OR issuer_name ILIKE :like
            OR invoice_number ILIKE :like
            OR external_id ILIKE :like
            OR id ILIKE :like
        """

        params = {
            "q": q,
            "like": f"%{q}%",
            "limit": limit,
            "offset": offset,
        }

        # numeric detection
        try:
            num = Decimal(q)
            sql += " OR amount_ht = :num OR amount_ttc = :num"
            params["num"] = num
        except InvalidOperation:
            pass

        sql += " ORDER BY created_at DESC LIMIT :limit OFFSET :offset"
        
        async with self._session as session:
            result = await session.execute(text(sql), params)
            invoices = result.mappings().all()
            return [Invoice(**invoice) for invoice in invoices]
    
    # async def update(
    #     self, 
    #     invoice: Invoice
    # ) -> Invoice:
    #     async with self._session as session:
    #         await session.merge(invoice)
    #         await session.commit()
    #         await session.refresh(invoice)
    #         return invoice

    async def get_external_invoice_id(self, invoice_id: str) -> str:
        async with self._session as session:
            cmd = "SELECT external_id FROM invoice WHERE id = :invoice_id"
            result = await session.execute(text(cmd), {"invoice_id": invoice_id})
            return result.scalar_one_or_none()