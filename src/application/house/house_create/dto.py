from src.application.common.dto import DTO


class HouseCreateDTO(DTO):
    entrances_count: int
    apartments_per_floor: int
    floors_count: int
    apartments_count: int
