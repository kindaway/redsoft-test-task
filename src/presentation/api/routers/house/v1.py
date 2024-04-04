from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.application.common.filter import Filter
from src.application.exceptions.repo import EntityNotFoundError
from src.application.house.house_create.dto import HouseCreateDTO
from src.application.house.house_create.usecase import HouseCreateUsecase
from src.application.house.house_delete.usecase import HouseDeleteUsecase
from src.application.house.house_get.usecase import HouseGetUsecase
from src.application.house.house_get_list.usecase import HouseGetListUsecase
from src.application.house.house_update.dto import HouseUpdateDTO
from src.application.house.house_update.usecase import HouseUpdateUsecase
from src.domain.common.exceptions import ValidationError
from src.domain.house.entity import House
from src.infrastructure.database.repositories.house import HouseRepo
from src.infrastructure.database.sqlalchemy_uow import SQLAlchemyUoW
from src.presentation.api.dependencies import get_session

house = APIRouter(prefix="/house", tags=["house"])


@house.post(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": House},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
    },
)
async def create_house(
        house_create: HouseCreateDTO, session: Annotated[AsyncSession, Depends(get_session)]
):
    repo = HouseRepo(session=session)
    uow = SQLAlchemyUoW(session=session)
    house_create = HouseCreateUsecase(house_create_dto=house_create, repo=repo, uow=uow)
    try:
        result = await house_create.execute()
        return result
    except ValidationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)


@house.put(
    path="/id/{id}",
    responses={
        status.HTTP_200_OK: {"model": House},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def update_house(
        id: int,
        house_update: HouseUpdateDTO,
        session: Annotated[AsyncSession, Depends(get_session)],
):
    repo = HouseRepo(session=session)
    uow = SQLAlchemyUoW(session=session)
    house_update = HouseUpdateUsecase(house_id=id, house_update_dto=house_update, repo=repo, uow=uow)
    try:
        result = await house_update.execute()
        return result
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
    except ValidationError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.details)


@house.delete(
    path="/id/{id}",
    responses={
        status.HTTP_200_OK: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def delete_house(
        id: int, session: Annotated[AsyncSession, Depends(get_session)]
):
    repo = HouseRepo(session=session)
    uow = SQLAlchemyUoW(session=session)
    house_delete = HouseDeleteUsecase(house_id=id, repo=repo, uow=uow)
    try:
        await house_delete.execute()
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)


@house.get(
    path="/id/{id}",
    responses={
        status.HTTP_200_OK: {"model": str},
        status.HTTP_404_NOT_FOUND: {"model": str},
    },
)
async def get_house(id: int, session: Annotated[AsyncSession, Depends(get_session)]):
    repo = HouseRepo(session=session)
    house_get = HouseGetUsecase(house_id=id, repo=repo)
    try:
        result = await house_get.execute()
        return result
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)


@house.get(
    path="/",
    responses={
        status.HTTP_200_OK: {"model": str},
    },
)
async def get_houses(session: Annotated[AsyncSession, Depends(get_session)], filter: Filter = Depends()):
    repo = HouseRepo(session=session)
    house_get = HouseGetListUsecase(filter=filter, repo=repo)
    try:
        result = await house_get.execute()
        return result
    except EntityNotFoundError as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=e.details)
