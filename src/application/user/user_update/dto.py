from src.application.common.dto import DTO


class UserUpdateDTO(DTO):
    first_name: str | None = None
    last_name: str | None = None
    patronymic: str | None = None
    apartment_number: int | None = None
    house_number: int | None = None
