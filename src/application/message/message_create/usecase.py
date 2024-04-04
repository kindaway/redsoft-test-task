import dataclasses

from src.application.common.dto import create_entity
from src.application.common.uow import IUoW
from src.application.common.usecase import Usecase
from src.application.message.message_create.dto import MessageCreateDTO
from src.application.message.repo import IMessageRepo
from src.application.friend.repo import IFriendRepo
from src.application.services.check_user_can_send_message import check_user_can_send_message
from src.application.user.repo import IUserRepo
from src.domain.common.exceptions import ValidationError, BusinessRuleBrokenError
from src.domain.message.entity import Message


@dataclasses.dataclass
class MessageCreateUsecase(Usecase):
    message_create_dto: MessageCreateDTO
    message_repo: IMessageRepo
    user_repo: IUserRepo
    friend_repo: IFriendRepo
    uow: IUoW

    async def execute(self) -> Message:
        user = await self.user_repo.get(id=self.message_create_dto.from_id)
        message_entity = create_entity(Message, self.message_create_dto)
        can_send = await check_user_can_send_message(user, self.message_create_dto.to_id, self.friend_repo)
        if not can_send:
            raise ValidationError(errors=[BusinessRuleBrokenError("can't send message to a user who is not your friend")])
        created_message = await self.message_repo.add(message_entity)
        await self.uow.commit()
        return created_message
