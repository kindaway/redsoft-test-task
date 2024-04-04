from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.common.filter import Filter
from src.application.exceptions.repo import EntityNotFoundError, EntityForeignKeyViolationError
from src.application.exceptions.services import ApartmentUnavailableError
from src.application.user.user_create.dto import UserCreateDTO
from src.application.user.user_create.usecase import UserCreateUsecase
from src.application.user.user_delete.usecase import UserDeleteUsecase
from src.application.user.user_get.usecase import UserGetUsecase
from src.application.user.user_get_list.usecase import UserGetListUsecase
from src.application.user.user_update.dto import UserUpdateDTO
from src.application.user.user_update.usecase import UserUpdateUsecase
from src.domain.common.exceptions import ValidationError
from src.domain.user.entity import User
from src.infrastructure.database.repositories.house import HouseRepo
from src.infrastructure.database.repositories.user import UserRepo
from src.infrastructure.database.sqlalchemy_uow import SQLAlchemyUoW
from src.presentation.api.dependencies import get_session

user = APIRouter(prefix="/user", tags=["user"])


@user.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": User},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_user(
        user_create: UserCreateDTO, session: Annotated[AsyncSession, Depends(get_session)]
):
    user_repo = UserRepo(session=session)
    house_repo = HouseRepo(session=session)
    uow = SQLAlchemyUoW(session=session)
    user_create = UserCreateUsecase(user_create_dto=user_create, user_repo=user_repo, house_repo=house_repo, uow=uow)
    try:
        result = await user_create.execute()
        return result
    except ValidationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    except EntityForeignKeyViolationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    except ApartmentUnavailableError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)


@user.put(
    path="/id/{id}",
    responses={
        status.HTTP_200_OK: {"model": User},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def update_user(
        id: int,
        user_update: UserUpdateDTO,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    user_repo = UserRepo(session=session)
    house_repo = HouseRepo(session=session)
    uow = SQLAlchemyUoW(session=session)
    user_update = UserUpdateUsecase(user_id=id, user_update_dto=user_update, user_repo=user_repo, house_repo=house_repo,
                                    uow=uow)
    try:
        result = await user_update.execute()
        return result
    except ValidationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    except EntityForeignKeyViolationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)
    except ApartmentUnavailableError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)


@user.delete(
    path="/id/{id}",
    responses={
        status.HTTP_200_OK: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_user(
        id: int, session: Annotated[AsyncSession, Depends(get_session)]
):
    repo = UserRepo(session=session)
    uow = SQLAlchemyUoW(session=session)
    user_delete = UserDeleteUsecase(user_id=id, repo=repo, uow=uow)
    try:
        await user_delete.execute()
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)


@user.get(
    path="/id/{id}",
    responses={
        status.HTTP_200_OK: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_user(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    repo = UserRepo(session=session)
    user_get = UserGetUsecase(user_id=id, repo=repo)
    try:
        result = await user_get.execute()
        return result
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)


@user.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": str},
    },
)
async def get_users(session: Annotated[AsyncSession, Depends(get_session)], filter: Filter = Depends()):
    repo = UserRepo(session=session)
    user_get = UserGetListUsecase(filter=filter, repo=repo)
    try:
        result = await user_get.execute()
        return result
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
