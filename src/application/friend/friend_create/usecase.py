import dataclasses

from src.application.common.dto import create_entity
from src.application.common.uow import IUoW
from src.application.common.usecase import Usecase
from src.application.friend.friend_create.dto import FriendCreateDTO
from src.application.friend.repo import IFriendRepo
from src.application.user.repo import IUserRepo
from src.domain.common.exceptions import ValidationError, BusinessRuleBrokenError
from src.domain.friend.entity import Friend


@dataclasses.dataclass
class FriendCreateUsecase(Usecase):
    friend_create_dto: FriendCreateDTO
    friend_repo: IFriendRepo
    user_repo: IUserRepo
    uow: IUoW

    async def execute(self) -> Friend:

        """Добавлять можно друга если
        1. номер квартиры отличается на один
        ИЛИ
        2. добавляемый человек -- друг соседа, т.е. у людей с номерами квартиры +-1 есть этот друг (реализовать в репе получение друзей человека)
        """

        friend_entity = create_entity(Friend, self.friend_create_dto)
        first_user = await self.user_repo.get(friend_entity.user_id)
        second_user = await self.user_repo.get(friend_entity.friend_id)

        neighbours = await self.user_repo.get_neighbours(first_user)
        neighbours_friends = []
        if neighbours:
            for n in neighbours:
                n_friends = await self.friend_repo.get_friends(user_id=n.id)
                neighbours_friends += n_friends

        neighbours_friend_ids = [x.id for x in neighbours_friends]

        same_house_cond = first_user.house_number == second_user.house_number
        close_neighbour = (first_user.apartment_number == second_user.apartment_number + 1) or (first_user.apartment_number == second_user.apartment_number - 1)
        neihbours_friend = second_user.id in neighbours_friend_ids

        if not (same_house_cond and (close_neighbour or neihbours_friend)):
            raise ValidationError(errors=BusinessRuleBrokenError("can't add a friend who is not a close neighbour or a neighbours' friend"))

        created_friend = await self.friend_repo.add(friend_entity)
        await self.uow.commit()
        return created_friend
