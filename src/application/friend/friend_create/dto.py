from src.application.common.dto import DTO


class FriendCreateDTO(DTO):
    user_id: int
    friend_id: int
