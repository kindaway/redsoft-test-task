import dataclasses

from src.application.common.filter import Filter
from src.application.common.usecase import Usecase
from src.application.user.repo import IUserRepo
from src.domain.user.entity import User


@dataclasses.dataclass
class UserGetListUsecase(Usecase):
    filter: Filter
    repo: IUserRepo

    async def execute(self) -> User:
        user_list = await self.repo.get_list(filter=self.filter)
        return user_list
