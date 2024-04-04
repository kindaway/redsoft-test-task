import dataclasses

from src.application.common.dto import mutate_entity
from src.application.common.uow import IUoW
from src.application.common.usecase import Usecase
from src.application.exceptions.services import ApartmentUnavailableError
from src.application.house.repo import IHouseRepo
from src.application.services.check_users_move_in import check_user_can_move_in
from src.application.user.repo import IUserRepo
from src.application.user.user_update.dto import UserUpdateDTO
from src.domain.user.entity import User


@dataclasses.dataclass
class UserUpdateUsecase(Usecase):
    user_id: int
    user_update_dto: UserUpdateDTO
    user_repo: IUserRepo
    house_repo: IHouseRepo
    uow: IUoW

    async def execute(self) -> User:
        user_entity = await self.user_repo.get(id=self.user_id)
        mutate_entity(user_entity, self.user_update_dto)
        can_move_in = await check_user_can_move_in(user_entity, self.house_repo)
        if not can_move_in:
            raise ApartmentUnavailableError
        await self.user_repo.add(user_entity)
        await self.uow.commit()
        return user_entity
