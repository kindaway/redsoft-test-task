import dataclasses

from src.application.common.uow import IUoW
from src.application.common.usecase import Usecase
from src.application.user.repo import IUserRepo


@dataclasses.dataclass
class UserDeleteUsecase(Usecase):
    user_id: int
    repo: IUserRepo
    uow: IUoW

    async def execute(self) -> bool:
        await self.repo.delete(self.user_id)
        await self.uow.commit()
