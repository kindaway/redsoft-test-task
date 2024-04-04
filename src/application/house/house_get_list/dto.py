from src.application.common.dto import DTO
from src.domain.house.entity import House


class HouseGetListResult(DTO):
    houses: list[House]
    total: int
    offset: int
    limit: int
