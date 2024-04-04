import dataclasses
from math import ceil

from src.application.common.dto import create_entity
from src.application.common.uow import IUoW
from src.application.common.usecase import Usecase
from src.application.exclusion_poll.exclusion_poll_create.dto import ExclusionPollCreateDTO
from src.application.exclusion_poll.repo import IExclusionPollRepo
from src.application.house.repo import IHouseRepo
from src.application.user.repo import IUserRepo
from src.domain.exclusion_poll.entity import ExclusionPoll


@dataclasses.dataclass
class ExclusionPollCreateUsecase(Usecase):
    exclusion_poll_create_dto: ExclusionPollCreateDTO
    exclusion_poll_repo: IExclusionPollRepo
    user_repo: IUserRepo
    house_repo: IHouseRepo
    uow: IUoW

    async def execute(self) -> ExclusionPoll:
        exclusion_poll_entity = create_entity(ExclusionPoll, self.exclusion_poll_create_dto)
        exclusion_candidate = await self.user_repo.get(self.exclusion_poll_create_dto.exclusion_candidate_id)
        people_count = await self.house_repo.get_people_count(house_id=exclusion_candidate.house_number)
        exclusion_poll_entity.votes_required = ceil(0.5 * people_count)
        exclusion_poll_entity.votes = 0
        created_exclusion_poll = await self.exclusion_poll_repo.add(exclusion_poll_entity)
        await self.uow.commit()
        return created_exclusion_poll
