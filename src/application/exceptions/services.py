from src.application.common.exceptions import ApplicationException


class ApartmentUnavailableError(ApplicationException):
    @property
    def details(self) -> str:
        return "Error: the apartment is occupied or doesn't exist"
