import abc

from src.application.common.filter import Filter
from src.application.user.user_get_list.dto import UserGetListResult
from src.domain.user.entity import User


class IUserRepo(abc.ABC):
    @abc.abstractmethod
    async def add(self, user: User) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    async def get(self, id: int) -> User:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_list(self, filter: Filter) -> UserGetListResult:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_count(self) -> int:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_neighbours(self, id: int) -> list[User]:
        raise NotImplementedError
