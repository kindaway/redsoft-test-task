from typing import Any, TypeVar, Type

from pydantic import BaseModel, model_validator

from src.domain.common.entities import DomainEntity

_T = TypeVar("_T", bound=DomainEntity)


class DTO(BaseModel):
    @model_validator(mode="before")
    def check_update_not_empty(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if all(x not in data for x in cls.model_fields):
                raise ValueError
            return data
        raise ValueError


def create_entity(entity: Type[_T], dto: DTO) -> _T:
    """Creates an entity with values provided in dto."""
    attrs = dto.model_dump(exclude_none=True)
    return entity(**attrs)


def mutate_entity(entity: DomainEntity, dto: DTO) -> None:
    for k, v in dto.model_dump(exclude_none=True).items():
        if hasattr(entity, k):
            setattr(entity, k, v)
    entity.validate()
