from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette.requests import Request


async def get_session(request: Request):
    session_maker: async_sessionmaker = request.app.state.session_pool
    async with session_maker() as s:
        yield s
