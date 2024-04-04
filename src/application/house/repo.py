import abc

from src.application.common.filter import Filter
from src.application.house.house_get_list.dto import HouseGetListResult
from src.domain.house.entity import House


class IHouseRepo(abc.ABC):
    @abc.abstractmethod
    async def add(self, house: House) -> House:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, id: int) -> House:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_list(self, filter: Filter) -> HouseGetListResult:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_count(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def is_apartment_available(self, user_id: int, house_id: int, apartment_number: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_people_count(self, house_id) -> int:
        raise NotImplementedError
