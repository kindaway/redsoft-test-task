import dataclasses

from src.application.common.usecase import Usecase
from src.application.house.repo import IHouseRepo
from src.domain.house.entity import House


@dataclasses.dataclass
class HouseGetUsecase(Usecase):
    house_id: int
    repo: IHouseRepo

    async def execute(self) -> House:
        house_entity = await self.repo.get(id=self.house_id)
        return house_entity
