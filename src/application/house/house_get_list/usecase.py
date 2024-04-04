import dataclasses

from src.application.common.filter import Filter
from src.application.common.usecase import Usecase
from src.application.house.repo import IHouseRepo
from src.domain.house.entity import House


@dataclasses.dataclass
class HouseGetListUsecase(Usecase):
    filter: Filter
    repo: IHouseRepo

    async def execute(self) -> House:
        house_list = await self.repo.get_list(filter=self.filter)
        return house_list
