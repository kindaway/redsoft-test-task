from typing import Iterable, Callable, AsyncContextManager, cast

from fastapi import FastAPI, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine


def setup_routers(
        app: FastAPI, routers: Iterable[APIRouter], prefix: str
):
    for router in routers:
        app.include_router(
            router=router,
            prefix=prefix,
        )


def setup_database(
        dsn: str,
) -> tuple[Callable[[], AsyncContextManager[AsyncSession]], AsyncEngine]:
    engine = create_async_engine(
        cast(str, dsn),
        pool_pre_ping=True,
    )

    session_pool = async_sessionmaker(
        bind=engine,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )

    return session_pool, engine
