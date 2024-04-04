import abc


class DomainEntity(abc.ABC):

    def __post_init__(self) -> None:
        self.validate()

    @abc.abstractmethod
    def validate(self) -> None:
        """:raises ValidationError: if the validation fails"""
        raise NotImplementedError
