from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.uow import IUoW


class SQLAlchemyUoW(IUoW):
    """SQLAlchemy Unit of Work"""

    def __init__(self, session: AsyncSession):
        self._session = session

    async def commit(self) -> bool:
        try:
            await self._session.commit()
            return True
        except IntegrityError:
            await self.rollback()
            return False

    async def rollback(self) -> None:
        await self._session.rollback()
