import dataclasses

from src.domain.common.entities import DomainEntity


@dataclasses.dataclass
class Friend(DomainEntity):
    user_id: int
    friend_id: int

    def validate(self) -> None:
        """Validation here is impossible since it requires having access to all of the other users in the house"""
        """hence business rules validation is implemented at the application level instead"""
        pass
