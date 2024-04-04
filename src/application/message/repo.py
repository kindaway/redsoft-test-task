import abc

from src.domain.message.entity import Message
from src.domain.user.entity import User


class IMessageRepo(abc.ABC):
    @abc.abstractmethod
    async def add(self, message: Message) -> Message:
        raise NotImplementedError

    @abc.abstractmethod
    async def get_messages(self, user_id: int) -> list[User]:
        raise NotImplementedError
