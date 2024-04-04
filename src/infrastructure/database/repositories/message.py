from sqlalchemy import select, or_
from sqlalchemy.exc import IntegrityError

from src.application.exceptions.repo import EntityForeignKeyViolationError
from src.application.message.repo import IMessageRepo
from src.domain.message.entity import Message
from src.domain.user.entity import User
from src.infrastructure.database.repositories.base import SQLAlchemyRepo


class MessageRepo(SQLAlchemyRepo, IMessageRepo):
    async def add(self, message: Message) -> Message:
        self.session.add(message)
        try:
            await self.session.flush()
            await self.session.refresh(message)
            return message
        except IntegrityError:
            raise EntityForeignKeyViolationError

    async def get_messages(self, user_id: int) -> list[User]:
        query = select(Message).where(or_(Message.from_id == user_id, Message.to_id == user_id))
        result = await self.session.scalars(query)
        return result.all()
