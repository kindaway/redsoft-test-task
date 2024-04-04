import pytest

from src.domain.common.exceptions import ValidationError
from src.domain.house.entity import House


def test_house_creation():
    House(
        id=1, entrances_count=2, apartments_per_floor=5, floors_count=10, apartments_count=100
    )
    with pytest.raises(ValidationError):
        House(
            id=1, entrances_count=2, apartments_per_floor=5, floors_count=10, apartments_count=101
        )
    with pytest.raises(ValidationError):
        House(
            id=1, entrances_count=-1, apartments_per_floor=5, floors_count=10, apartments_count=100
        )

