import abc

from src.domain.friend.entity import Friend
from src.domain.user.entity import User


class IFriendRepo(abc.ABC):
    @abc.abstractmethod
    async def add(self, friend: Friend) -> Friend:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, user_id: int, friend_id: int) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def are_friends(self, user_id: int, friend_id: int) -> bool:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_friends(self, user_id: int) -> list[User]:
        raise NotImplementedError
