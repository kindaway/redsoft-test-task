from src.application.common.dto import DTO


class MessageCreateDTO(DTO):
    from_id: int
    to_id: int
    text: str
