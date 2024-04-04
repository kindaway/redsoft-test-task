from sqlalchemy import select, exists, or_, and_, delete, union
from sqlalchemy.exc import IntegrityError

from src.application.exceptions.repo import EntityNotFoundError, EntityForeignKeyViolationError
from src.application.friend.repo import IFriendRepo
from src.domain.friend.entity import Friend
from src.domain.user.entity import User
from src.infrastructure.database.models import users
from src.infrastructure.database.repositories.base import SQLAlchemyRepo


class FriendRepo(SQLAlchemyRepo, IFriendRepo):
    async def add(self, friend: Friend) -> Friend:
        self.session.add(friend)
        try:
            await self.session.flush()
            await self.session.refresh(friend)
            return friend
        except IntegrityError:
            raise EntityForeignKeyViolationError

    async def are_friends(self, user_id: int, friend_id: int) -> bool:
        query = select(
            exists(Friend).where(
                or_(
                    and_(Friend.user_id == user_id, Friend.friend_id == friend_id),
                    and_(Friend.user_id == friend_id, Friend.friend_id == user_id)
                )
            )
        )
        result = await self.session.scalar(query)
        return result

    async def delete(self, user_id: int, friend_id: int) -> None:
        friend_exists = await self.are_friends(user_id, friend_id)
        if not friend_exists:
            raise EntityNotFoundError
        query = delete(Friend).where(
            or_(
                and_(Friend.user_id == user_id, Friend.friend_id == friend_id),
                and_(Friend.user_id == friend_id, Friend.friend_id == user_id)
            )
        )
        await self.session.execute(query)

    async def get_friends(self, user_id: int) -> list[User]:
        subquery = union(
            select(Friend.friend_id).where(Friend.user_id == user_id),
            select(Friend.user_id).where(Friend.friend_id == user_id)
        )
        query = select(User).where(
            users.c.id.in_(subquery)
        )
        result = await self.session.scalars(query)
        return result.all()
