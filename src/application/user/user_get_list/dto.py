from src.application.common.dto import DTO
from src.domain.user.entity import User


class UserGetListResult(DTO):
    users: list[User]
    total: int
    offset: int
    limit: int
