from domain.models.invoice import Invoice, EnumInvoiceStatus
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc, or_, and_, text
from decimal import Decimal, InvalidOperation
from typing import Optional, Tuple, List
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
        page: int = 1,
        limit: int = 30,
        query: Optional[str] = None
    ) -> Tuple[List[Invoice] | None, int]:
        
        offset = (page - 1) * limit
        conditions = []
        params = {"limit": limit, "offset": offset}

        # --- Status filter ---
        if status and status != "All":
            conditions.append("status = :status")
            params.update({"status": status})

        # --- Search query filter ---
        if query:
            search_conditions = [
                "search_vector @@ plainto_tsquery(:q)",
                "issuer_name ILIKE :like",
                "invoice_number ILIKE :like",
                "external_id ILIKE :like",
                "id ILIKE :like"
            ]
            params.update({"q": query, "like": f"%{query}%"})

            # Numeric detection (amount_ht / amount_ttc)
            try:
                num = Decimal(query)
                search_conditions.append("amount_ht = :num OR amount_ttc = :num")
                params.update({"num": num})
            except InvalidOperation:
                pass

            # Ajouter le search_conditions à la clause WHERE
            conditions.append("(" + " OR ".join(search_conditions) + ")")

        print('@CONDITIONS : ', conditions)
        print('@PARAMS : ', params)
        # --- Construire le WHERE complet ---
        where_clause = f"WHERE {' AND '.join(conditions)}" if conditions else ""
        
        print('@QUERY SQL : ', where_clause)
        print('@PARAMS : ', params)

        # --- Requête principale avec pagination ---
        query_sql = f"""
        {QUERY_GET_ALL_INVOICES}
        {where_clause}
        ORDER BY created_at DESC, id DESC
        LIMIT :limit OFFSET :offset
        """
        
        print('@QUERY SQL : ', text(query_sql))

        # --- Requête count pour total ---
        count_sql = f"""
        SELECT COUNT(*) AS total_count FROM invoice
        {where_clause}
        """

        async with self._session() as session:
            result_items = await session.execute(text(query_sql), params)
            invoices_rows = result_items.mappings().all()
            print('@INVOICES ROWS : ', invoices_rows)

            # Fetch total count
            result_count = await session.execute(text(count_sql), params)
            total_count = result_count.scalar_one()
            print('@TOTAL COUNT : ', total_count)
                
        return [
            Invoice(**row)
            for row in invoices_rows
        ] if invoices_rows else None, total_count

    async def get_by_id(
        self,
        id: str
    ) -> Invoice:
        async with self._session() as session:
            stmt = select(Invoice).where(
                (Invoice.id == id) |
                (Invoice.external_id == id)
            )

            result = await session.execute(stmt)
            return result.scalar_one_or_none()

    
    async def get_last_invoice_id(self) -> Optional[str]:
        async with self._session() as session:
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
        async with self._session() as session:
            result = await session.execute(
                text(query),
                { "external_ids" : external_ids }
            )
            invoices = result.mappings().all()
            return [Invoice(**row) for row in invoices]
        
    
    async def search(
        self, 
        q: str, 
        limit: int = 30, 
        offset: int = 0 ) -> list[Invoice]:
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
        
        async with self._session() as session:
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
        async with self._session() as session:
            cmd = "SELECT external_id FROM invoice WHERE id = :invoice_id"
            result = await session.execute(text(cmd), {"invoice_id": invoice_id})
            return result.scalar_one_or_none()