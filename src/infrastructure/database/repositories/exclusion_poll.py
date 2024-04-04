from sqlalchemy import delete
from sqlalchemy.exc import IntegrityError

from src.application.exceptions.repo import EntityForeignKeyViolationError
from src.application.exclusion_poll.repo import IExclusionPollRepo
from src.domain.exclusion_poll.entity import ExclusionPoll
from src.infrastructure.database.repositories.base import SQLAlchemyRepo


class ExclusionPollRepo(SQLAlchemyRepo, IExclusionPollRepo):
    async def add(self, exclusion_poll: ExclusionPoll) -> ExclusionPoll:
        self.session.add(exclusion_poll)
        try:
            await self.session.flush()
            await self.session.refresh(exclusion_poll)
            return exclusion_poll
        except IntegrityError:
            raise EntityForeignKeyViolationError

    async def delete(self, exclusion_candidate_id: int) -> None:
        query = delete(ExclusionPoll).where(
            ExclusionPoll.exclusion_candidate_id == exclusion_candidate_id
        )
        await self.session.execute(query)

    async def upvote(self, id: int) -> ExclusionPoll:
        exclusion_poll = await self.session.get(ExclusionPoll, id)
        exclusion_poll.votes += 1
        return exclusion_poll

    async def downvote(self, id: int) -> ExclusionPoll:
        exclusion_poll = await self.session.get(ExclusionPoll, id)
        exclusion_poll.votes -= 1
        return exclusion_poll
