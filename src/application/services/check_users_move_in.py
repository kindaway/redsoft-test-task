from src.application.house.repo import IHouseRepo
from src.domain.user.entity import User


async def check_user_can_move_in(user: User, house_repo: IHouseRepo) -> bool:
    result = await house_repo.is_apartment_available(house_id=user.house_number, apartment_number=user.apartment_number, user_id=user.id)
    return result
