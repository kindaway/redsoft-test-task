from src.application.common.dto import create_entity
from src.application.house.house_create.dto import HouseCreateDTO
from src.domain.house.entity import House


def test_create_entity_from_dto():
    dto = HouseCreateDTO(floors_count=1, apartments_per_floor=10, entrances_count=1, apartments_count=10)
    entity = create_entity(House, dto)
    assert entity == House(entrances_count=1, apartments_per_floor=10, floors_count=1, apartments_count=10, id=None)

# def test_mutate_entity():
#     dto = HouseCreateDTO(floors_count=1, apartments_per_floor=10, entrances_count=1, apartments_count=10)
#     house = create_entity(House, dto)
#     assert house.floors_count == 1
#     update_dto = HouseCreateDTO(floors_count=1)
#     mutate_entity(house,)
