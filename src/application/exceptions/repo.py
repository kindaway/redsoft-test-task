from src.application.common.exceptions import ApplicationException


class EntityNotFoundError(ApplicationException):
    def __init__(self, id: int):
        self.entity_id = id

    @property
    def details(self) -> str:
        return f"Entity not found: id {self.entity_id}"


class EntityForeignKeyViolationError(ApplicationException):
    def __init__(self, fk_id: int | None = None):
        self.fk_id = fk_id

    @property
    def details(self) -> str:
        if self.fk_id:
            return f"Can't assign to non-existent entity with id {self.fk_id}"
        return "Can't assign to non-existent entity"
