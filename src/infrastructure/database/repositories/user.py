from sqlalchemy import select, func, and_, or_
from sqlalchemy.exc import IntegrityError

from src.application.common.filter import Filter, OrderFilter
from src.application.exceptions.repo import EntityNotFoundError, EntityForeignKeyViolationError
from src.application.user.repo import IUserRepo
from src.application.user.user_get_list.dto import UserGetListResult
from src.domain.user.entity import User
from src.infrastructure.database.models import users
from src.infrastructure.database.repositories.base import SQLAlchemyRepo


class UserRepo(SQLAlchemyRepo, IUserRepo):
    async def add(self, user: User) -> User:
        self.session.add(user)
        try:
            await self.session.flush()
            await self.session.refresh(user)
            return user
        except IntegrityError:
            raise EntityForeignKeyViolationError(fk_id=user.house_number)

    async def get(self, id: int) -> User:
        result = await self.session.get(User, id)
        if not result:
            raise EntityNotFoundError(id=id)
        return result

    async def delete(self, id: int) -> None:
        user = await self.get(id)
        await self.session.delete(user)

    async def get_list(self, filter: Filter) -> list[UserGetListResult]:
        query = select(User)
        if filter.order is OrderFilter.ASC:
            query = query.order_by(users.c.id.asc())
        else:
            query = query.order_by(users.c.id.desc())

        if filter.offset:
            query = query.offset(filter.offset)

        if filter.limit:
            query = query.limit(filter.limit)

        count = await self.get_count()
        results = await self.session.scalars(query)
        return UserGetListResult(
            users=results,
            total=count,
            offset=filter.offset,
            limit=filter.limit,
        )

    async def get_count(self) -> int:
        return (
            await self.session.scalar(
                select(func.count())
                .select_from(users)
            )
        ) or 0

    async def get_neighbours(self, user: User) -> list[User]:
        query = select(User).where(
            and_(
                User.house_number == user.house_number,
                or_(
                    User.apartment_number == user.apartment_number + 1,
                    User.apartment_number == user.apartment_number - 1
                )
            )
        )
        result = await self.session.scalars(query)
        neighbours = result.all()
        return neighbours
