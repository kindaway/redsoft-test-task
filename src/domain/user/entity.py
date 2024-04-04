import dataclasses
from typing import Optional

from src.domain.common.entities import DomainEntity


@dataclasses.dataclass
class User(DomainEntity):
    first_name: str
    last_name: str
    patronymic: str
    apartment_number: int
    house_number: int
    id: Optional[int] = None

    def validate(self) -> None:
        pass
