from src.application.common.dto import DTO


class UserCreateDTO(DTO):
    first_name: str
    last_name: str
    patronymic: str
    apartment_number: int
    house_number: int
