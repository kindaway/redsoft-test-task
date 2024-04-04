import asyncio

import uvicorn
from dynaconf import Dynaconf
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import AsyncEngine

from src.infrastructure.database.models import map_domain
from src.presentation.api.routers.exclusion_poll.v1 import exclusion_poll
from src.presentation.api.routers.friend.v1 import friend
from src.presentation.api.routers.house.v1 import house
from src.presentation.api.routers.message.v1 import message
from src.presentation.api.routers.user.v1 import user
from src.presentation.api.setup import setup_routers, setup_database


class ApiApplication:
    def __init__(
            self,
            config: Dynaconf,
            fastapi_app: FastAPI,
            db_engine: AsyncEngine,
    ) -> None:
        self._config = config
        self._app = fastapi_app
        self._db_engine = db_engine

    @classmethod
    async def from_config(cls, settings_path: str) -> "ApiApplication":
        config = Dynaconf(
            envvar_prefix="DYNACONF",
            settings_files=[
                settings_path + "/settings.toml",
                settings_path + "/.secrets.toml",
            ],
        )

        fastapi_app = FastAPI(title=config.api.project_name, docs_url=config.api.prefix + "/docs")
        setup_routers(
            app=fastapi_app,
            routers=[
                house,
                user,
                friend,
                message,
                exclusion_poll
            ],
            prefix=config.api.prefix
        )
        fastapi_app.state.config = config

        session_pool, db_engine = setup_database(dsn=config.database.url)
        map_domain()
        fastapi_app.state.session_pool = session_pool

        application = ApiApplication(
            config=config,
            fastapi_app=fastapi_app,
            db_engine=db_engine
        )

        return application

    async def run(self):
        try:
            server = uvicorn.Server(
                config=uvicorn.Config(
                    app=self._app,
                    host=self._config.api.host,
                    port=int(self._config.api.port)
                )
            )
            await server.serve()
        except asyncio.CancelledError:
            print("HTTP server has been interrupted")

    async def shutdown(self):
        dispose_errors = []

        try:
            await self._db_engine.dispose()
        except Exception as unexpected_error:
            dispose_errors.append(unexpected_error)

        if dispose_errors:
            print("Application has shut down with errors")
