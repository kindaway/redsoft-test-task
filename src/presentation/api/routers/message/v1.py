from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.exceptions.repo import EntityForeignKeyViolationError, EntityNotFoundError
from src.application.exceptions.services import ApartmentUnavailableError
from src.application.message.message_create.dto import MessageCreateDTO
from src.application.message.message_create.usecase import MessageCreateUsecase
from src.domain.common.exceptions import ValidationError
from src.domain.message.entity import Message
from src.infrastructure.database.repositories.friend import FriendRepo
from src.infrastructure.database.repositories.message import MessageRepo
from src.infrastructure.database.repositories.user import UserRepo
from src.infrastructure.database.sqlalchemy_uow import SQLAlchemyUoW
from src.presentation.api.dependencies import get_session

message = APIRouter(prefix="/message", tags=["message"])


@message.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Message},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_message(
        message_create: MessageCreateDTO, session: Annotated[AsyncSession, Depends(get_session)]
):
    message_repo = MessageRepo(session=session)
    user_repo = UserRepo(session=session)
    friend_repo = FriendRepo(session=session)
    uow = SQLAlchemyUoW(session=session)
    message_create = MessageCreateUsecase(message_create_dto=message_create, message_repo=message_repo,
                                          user_repo=user_repo, friend_repo=friend_repo, uow=uow)
    try:
        result = await message_create.execute()
        return result
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    except ValidationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    except EntityForeignKeyViolationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    except ApartmentUnavailableError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
