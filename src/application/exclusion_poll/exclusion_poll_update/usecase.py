import dataclasses

from src.application.common.uow import IUoW
from src.application.common.usecase import Usecase
from src.application.exclusion_poll.repo import IExclusionPollRepo
from src.application.user.repo import IUserRepo


@dataclasses.dataclass
class ExclusionPollUpdateUsecase(Usecase):
    candidate_id: int
    exclude: bool
    user_repo: IUserRepo
    exclusion_poll_repo: IExclusionPollRepo
    uow: IUoW

    async def execute(self) -> bool:
        """returns True if user has been excluded and False if not"""
        if self.exclude:
            exclusion_poll = await self.exclusion_poll_repo.downvote(id=self.candidate_id)
        else:
            exclusion_poll = await self.exclusion_poll_repo.upvote(id=self.candidate_id)

        if exclusion_poll.votes >= exclusion_poll.votes_required:
            await self.exclusion_poll_repo.delete(exclusion_poll.exclusion_candidate_id)
            await self.user_repo.delete(id=exclusion_poll.exclusion_candidate_id)
            await self.uow.commit()
            return True
        else:
            await self.uow.commit()
            return False

