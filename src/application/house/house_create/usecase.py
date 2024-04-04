import dataclasses

from src.application.common.dto import create_entity
from src.application.common.uow import IUoW
from src.application.common.usecase import Usecase
from src.application.house.house_create.dto import HouseCreateDTO
from src.application.house.repo import IHouseRepo
from src.domain.house.entity import House


@dataclasses.dataclass
class HouseCreateUsecase(Usecase):
    house_create_dto: HouseCreateDTO
    repo: IHouseRepo
    uow: IUoW

    async def execute(self) -> House:
        house_entity = create_entity(House, self.house_create_dto)
        created_house = await self.repo.add(house_entity)
        await self.uow.commit()
        return created_house
