import dataclasses
from typing import Optional

from src.domain.common.entities import DomainEntity
from src.domain.common.exceptions import ValidationError, BusinessRuleBrokenError


@dataclasses.dataclass
class Message(DomainEntity):
    from_id: int
    to_id: int
    text: str
    id: Optional[int] = None

    def validate(self) -> None:
        if not self.text:
            raise ValidationError(errors=[BusinessRuleBrokenError("text cannot be empty")])
