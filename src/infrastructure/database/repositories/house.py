from sqlalchemy import select, func, exists, and_
from sqlalchemy.sql.functions import count

from src.application.common.filter import Filter, OrderFilter
from src.application.exceptions.repo import EntityNotFoundError
from src.application.house.house_get_list.dto import HouseGetListResult
from src.application.house.repo import IHouseRepo
from src.domain.house.entity import House
from src.domain.user.entity import User
from src.infrastructure.database.models import houses, users
from src.infrastructure.database.repositories.base import SQLAlchemyRepo


class HouseRepo(SQLAlchemyRepo, IHouseRepo):
    async def add(self, house: House) -> House:
        self.session.add(house)
        await self.session.flush()
        await self.session.refresh(house)
        return house

    async def get(self, id: int) -> House:
        result = await self.session.get(House, id)
        if not result:
            raise EntityNotFoundError(id=id)
        return result

    async def delete(self, id: int) -> None:
        house = await self.get(id)
        await self.session.delete(house)

    async def get_list(self, filter: Filter) -> list[HouseGetListResult]:
        query = select(House)
        if filter.order is OrderFilter.ASC:
            query = query.order_by(houses.c.id.asc())
        else:
            query = query.order_by(houses.c.id.desc())

        if filter.offset:
            query = query.offset(filter.offset)

        if filter.limit:
            query = query.limit(filter.limit)

        count = await self.get_count()
        results = await self.session.scalars(query)
        return HouseGetListResult(
            houses=results,
            total=count,
            offset=filter.offset,
            limit=filter.limit,
        )

    async def get_count(self) -> int:
        return (
            await self.session.scalar(
                select(func.count())
                .select_from(houses)
            )
        ) or 0

    async def is_apartment_available(self, user_id: int, house_id: int, apartment_number: int) -> bool:
        query = select(
            exists(User).where(and_(User.id != user_id, User.apartment_number == apartment_number, User.house_number == house_id))
        )
        apartment_available = not await self.session.scalar(query)
        house = await self.get(house_id)
        apartment_exists = 0 < apartment_number <= house.apartments_count

        return apartment_exists and apartment_available

    async def get_people_count(self, house_id) -> int:
        query = select(count(User.id)).select_from(users).where(users.c.house_number == house_id)
        result = await self.session.scalar(query)
        return result
