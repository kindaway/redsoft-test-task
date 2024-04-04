import dataclasses

from src.application.common.dto import mutate_entity
from src.application.common.uow import IUoW
from src.application.common.usecase import Usecase
from src.application.house.house_update.dto import HouseUpdateDTO
from src.application.house.repo import IHouseRepo
from src.domain.house.entity import House


@dataclasses.dataclass
class HouseUpdateUsecase(Usecase):
    house_id: int
    house_update_dto: HouseUpdateDTO
    repo: IHouseRepo
    uow: IUoW

    async def execute(self) -> House:
        house_entity = await self.repo.get(id=self.house_id)
        mutate_entity(house_entity, self.house_update_dto)
        await self.repo.add(house_entity)
        await self.uow.commit()
        return house_entity
