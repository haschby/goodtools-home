from typing import Callable, List, Optional, Tuple, Dict

from sqlalchemy import select, update, text, bindparam
from sqlalchemy.ext.asyncio import AsyncSession

from application.ports.buybackRepository import BuybackRepositoryPort
from domain.models.buyback import Buyback
from application.dtos.buybackDto import BuybackPatchSchema


class BuybackRepositoryImpl(BuybackRepositoryPort):
    """Outbound adapter persisting buybacks in PostgreSQL via SQLAlchemy.

    The transaction boundary lives here: either every buyback in the batch is
    inserted, or none of them is (the ``async with session`` context rolls back
    on any exception).
    """

    def __init__(self, session: Callable[[], AsyncSession]) -> None:
        self._session = session

    async def save_all(self, buybacks: List[Buyback]) -> List[Buyback]:
        async with self._session() as session:
            async with session.begin():
                session.add_all(buybacks)
            for buyback in buybacks:
                await session.refresh(buyback)
            return buybacks

    async def find_by_ids(self, ids: List[str]) -> List[Buyback]:
        if not ids:
            return []
        async with self._session() as session:
            stmt = (
                select(Buyback)
                .where(Buyback.id.in_(ids))
                .order_by(Buyback.created_at, Buyback.id)
            )
            result = await session.execute(stmt)
            return list(result.scalars().all())

    async def find_by_id(self, buyback_id: str) -> Optional[Buyback]:
        if not buyback_id:
            return None
        async with self._session() as session:
            stmt = select(Buyback).where(Buyback.id == buyback_id)
            result = await session.execute(stmt)
            return result.scalars().first()
    
    async def find_all(self) -> List[Buyback]:
        pass
    
    async def get_all(
        self,
        status: Optional[str] = "All",
        page: int = 1,
        limit: int = 30,
        query: Optional[str] = None
    ) -> Tuple[List[Buyback], List[dict], int]:
        offset = (page - 1) * limit
        allowed_statuses = ["A Traiter", "Valider"]

        conditions = ["status IN :allowed_statuses"]
        params = {
            "limit": limit,
            "offset": offset,
            "allowed_statuses": allowed_statuses,
        }

        # --- Status filter ---
        if status and status != "All":
            conditions.append("status = :status")
            params.update({"status": status})

        where_clause = f"WHERE {' AND '.join(conditions)}"

        query_sql = f"""
        SELECT *
        FROM buyback
        {where_clause}
        ORDER BY created_at, id DESC
        LIMIT :limit OFFSET :offset
        """

        count_sql = """
        SELECT status, COUNT(*) AS total
        FROM buyback
        WHERE status IN :allowed_statuses
        GROUP BY status
        ORDER BY status
        """

        async with self._session() as session:
            items_stmt = text(query_sql).bindparams(
                bindparam("allowed_statuses", expanding=True)
            )
            result_items = await session.execute(items_stmt, params)
            buyback_rows = result_items.mappings().all()

            count_stmt = text(count_sql).bindparams(
                bindparam("allowed_statuses", expanding=True)
            )
            result_count = await session.execute(
                count_stmt,
                {"allowed_statuses": allowed_statuses},
            )
            count_by_status = result_count.mappings().all()
            total = sum(row["total"] for row in count_by_status)

        items = [Buyback(**row) for row in buyback_rows]
        return items, count_by_status, total
    
    async def patch(self, buyback: BuybackPatchSchema) -> Buyback:
        print("buyback", buyback)
        async with self._session() as session:
            stmt = (
                update(Buyback)
                .where(Buyback.id == buyback.id)
                .values(buyback.model_dump(exclude_unset=True))
                .returning(Buyback)
            )

            result = await session.execute(stmt)
            await session.commit()

            updated_buyback = result.scalar_one()

            print("result", updated_buyback)
            return updated_buyback
