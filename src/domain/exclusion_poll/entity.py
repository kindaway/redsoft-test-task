import dataclasses

from src.domain.common.entities import DomainEntity
from src.domain.common.exceptions import BusinessRuleBrokenError, ValidationError


@dataclasses.dataclass
class ExclusionPoll(DomainEntity):
    exclusion_candidate_id: int
    reason: str
    votes: int | None = None
    votes_required: int | None = None

    def validate(self) -> None:
        errors = []
        # if self.votes_required <= 0:
        #     errors.append(BusinessRuleBrokenError("required votes cannot be equal or less than 0"))
        if not self.reason:
            errors.append(BusinessRuleBrokenError("can't exclude a member without a reason"))

        if errors:
            raise ValidationError(errors=errors)
