from enum import Enum

from src.application.common.dto import DTO


class OrderFilter(Enum):
    ASC = "asc"
    DESC = "desc"


class Filter(DTO):
    offset: int = 0
    limit: int = 0
    order: OrderFilter = OrderFilter.ASC
