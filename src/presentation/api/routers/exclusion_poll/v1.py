from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.exceptions.repo import EntityForeignKeyViolationError, EntityNotFoundError
from src.application.exceptions.services import ApartmentUnavailableError
from src.application.exclusion_poll.exclusion_poll_create.dto import ExclusionPollCreateDTO
from src.application.exclusion_poll.exclusion_poll_create.usecase import ExclusionPollCreateUsecase
from src.application.exclusion_poll.exclusion_poll_update.dto import ExclusionPollUpdateDTO
from src.application.exclusion_poll.exclusion_poll_update.usecase import ExclusionPollUpdateUsecase
from src.domain.common.exceptions import ValidationError
from src.domain.exclusion_poll.entity import ExclusionPoll
from src.infrastructure.database.repositories.exclusion_poll import ExclusionPollRepo
from src.infrastructure.database.repositories.house import HouseRepo
from src.infrastructure.database.repositories.user import UserRepo
from src.infrastructure.database.sqlalchemy_uow import SQLAlchemyUoW
from src.presentation.api.dependencies import get_session

exclusion_poll = APIRouter(prefix="/exclusion_poll", tags=["exclusion_poll"])


@exclusion_poll.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": ExclusionPoll},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_exclusion_poll(
        exclusion_poll_create: ExclusionPollCreateDTO, session: Annotated[AsyncSession, Depends(get_session)]
):
    exclusion_poll_repo = ExclusionPollRepo(session=session)
    user_repo = UserRepo(session=session)
    house_repo = HouseRepo(session=session)
    uow = SQLAlchemyUoW(session=session)
    exclusion_poll_create = ExclusionPollCreateUsecase(exclusion_poll_create_dto=exclusion_poll_create,
                                                       exclusion_poll_repo=exclusion_poll_repo,
                                                       user_repo=user_repo, house_repo=house_repo, uow=uow)
    try:
        result = await exclusion_poll_create.execute()
        return result
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    except ValidationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    except EntityForeignKeyViolationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    except ApartmentUnavailableError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)



@exclusion_poll.put(
    path="/id/{id}",
    responses={
        status.HTTP_200_OK: {"model": ExclusionPoll},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def update_exclusion_poll(
        id: int,
        exclude: ExclusionPollUpdateDTO,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    user_repo = UserRepo(session=session)
    exclusion_poll_repo = ExclusionPollRepo(session=session)
    uow = SQLAlchemyUoW(session=session)
    exclusion_poll_update = ExclusionPollUpdateUsecase(candidate_id=id, exclude=exclude.exclude, uow=uow, user_repo=user_repo, exclusion_poll_repo=exclusion_poll_repo)
    try:
        result = await exclusion_poll_update.execute()
        return result
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    except ValidationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)