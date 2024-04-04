class DomainException(Exception):
    pass


class BusinessRuleBrokenError(DomainException):
    pass


class ValidationError(DomainException):
    def __init__(self, errors: list[Exception]):
        self.errors = errors

    @property
    def details(self):
        text = "; ".join(tuple(str(x) for x in self.errors))
        return "Errors: " + text
