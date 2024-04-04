import abc

from src.domain.exclusion_poll.entity import ExclusionPoll


class IExclusionPollRepo(abc.ABC):
    @abc.abstractmethod
    async def add(self, exclusion_poll: ExclusionPoll) -> ExclusionPoll:
        raise NotImplementedError

    @abc.abstractmethod
    async def delete(self, id) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    async def upvote(self, id: int) -> ExclusionPoll:
        raise NotImplementedError

    @abc.abstractmethod
    async def downvote(self, id: int) -> ExclusionPoll:
        raise NotImplementedError
