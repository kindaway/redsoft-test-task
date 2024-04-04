from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.exceptions.repo import EntityForeignKeyViolationError, EntityNotFoundError
from src.application.exceptions.services import ApartmentUnavailableError
from src.application.friend.friend_create.dto import FriendCreateDTO
from src.application.friend.friend_create.usecase import FriendCreateUsecase
from src.domain.common.exceptions import ValidationError
from src.domain.friend.entity import Friend
from src.infrastructure.database.repositories.friend import FriendRepo
from src.infrastructure.database.repositories.user import UserRepo
from src.infrastructure.database.sqlalchemy_uow import SQLAlchemyUoW
from src.presentation.api.dependencies import get_session

friend = APIRouter(prefix="/friend", tags=["friend"])


@friend.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": Friend},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_friend(
        friend_create: FriendCreateDTO, session: Annotated[AsyncSession, Depends(get_session)]
):
    friend_repo = FriendRepo(session=session)
    user_repo = UserRepo(session=session)
    uow = SQLAlchemyUoW(session=session)
    friend_create = FriendCreateUsecase(friend_create_dto=friend_create, friend_repo=friend_repo, user_repo=user_repo,
                                        uow=uow)
    try:
        result = await friend_create.execute()
        return result
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.details)
    except ValidationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    except EntityForeignKeyViolationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    except ApartmentUnavailableError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
