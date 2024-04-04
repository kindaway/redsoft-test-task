import dataclasses
from typing import Optional

from src.domain.common.entities import DomainEntity
from src.domain.common.exceptions import BusinessRuleBrokenError, ValidationError


@dataclasses.dataclass
class House(DomainEntity):
    entrances_count: int
    apartments_per_floor: int
    floors_count: int
    apartments_count: int
    id: Optional[int] = None

    def validate(self) -> None:
        errors = []
        if not (self.apartments_count == (self.apartments_per_floor * self.floors_count) * self.entrances_count):
            errors.append(BusinessRuleBrokenError("apartments count and floors count do not add up"))

        if any((
                self.entrances_count <= 0,
                self.apartments_per_floor <= 0,
                self.floors_count <= 0,
                self.apartments_count <= 0
        )):
            errors.append(BusinessRuleBrokenError("some attributes are equal to 0 or are lesser than 0"))
        if errors:
            raise ValidationError(errors)
