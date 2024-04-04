from src.application.friend.repo import IFriendRepo
from src.domain.user.entity import User


async def check_user_can_send_message(user: User, to_id: int, friend_repo: IFriendRepo) -> bool:
    result = await friend_repo.are_friends(user_id=user.id, friend_id=to_id)
    return result
