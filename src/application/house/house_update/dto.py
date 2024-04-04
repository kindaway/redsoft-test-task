from src.application.common.dto import DTO


class HouseUpdateDTO(DTO):
    entrances_count: int | None = None
    apartments_per_floor: int | None = None
    floors_count: int | None = None
    apartments_count: int | None = None
