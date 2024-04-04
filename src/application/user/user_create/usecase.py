import dataclasses

from src.application.common.dto import create_entity
from src.application.common.uow import IUoW
from src.application.common.usecase import Usecase
from src.application.exceptions.services import ApartmentUnavailableError
from src.application.house.repo import IHouseRepo
from src.application.services.check_users_move_in import check_user_can_move_in
from src.application.user.user_create.dto import UserCreateDTO
from src.application.user.repo import IUserRepo
from src.domain.user.entity import User


@dataclasses.dataclass
class UserCreateUsecase(Usecase):
    user_create_dto: UserCreateDTO
    user_repo: IUserRepo
    house_repo: IHouseRepo
    uow: IUoW

    async def execute(self) -> User:
        user_entity = create_entity(User, self.user_create_dto)
        can_move_in = await check_user_can_move_in(user_entity, self.house_repo)
        if not can_move_in:
            raise ApartmentUnavailableError
        created_user = await self.user_repo.add(user_entity)
        await self.uow.commit()
        return created_user
