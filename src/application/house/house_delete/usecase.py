import dataclasses

from src.application.common.uow import IUoW
from src.application.common.usecase import Usecase
from src.application.house.repo import IHouseRepo


@dataclasses.dataclass
class HouseDeleteUsecase(Usecase):
    house_id: int
    repo: IHouseRepo
    uow: IUoW

    async def execute(self) -> bool:
        await self.repo.delete(self.house_id)
        await self.uow.commit()
