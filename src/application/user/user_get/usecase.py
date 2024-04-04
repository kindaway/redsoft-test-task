import dataclasses

from src.application.common.usecase import Usecase
from src.application.user.repo import IUserRepo
from src.domain.user.entity import User


@dataclasses.dataclass
class UserGetUsecase(Usecase):
    user_id: int
    repo: IUserRepo

    async def execute(self) -> User:
        user_entity = await self.repo.get(id=self.user_id)
        return user_entity
