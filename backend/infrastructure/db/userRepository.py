from domain.models.user import User, Role
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import Optional
from .baseRepository import BaseRepository

class UserRepositoryImpl(BaseRepository[User]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, User)
    
    async def get_all(self, role: Optional[str] = "admin") -> list[User]:
        command = select(User).order_by(desc(User.created_at))
        if role and role != "admin":
            command = command.where(User.role == role)
        
        result = await self._session.execute(command)
        return result.scalars().all()

    async def get_by_id(self, id: str) -> User:
        result = await self._session.execute(
            select(User).where(User.id == id)
        )
        return result.scalar_one_or_none()

    async def update(self, user: User) -> User:
        self._session.add(user)
        await self._session.commit()
        await self._session.refresh(user)
        return invoice