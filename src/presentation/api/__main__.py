import asyncio
import os

from src.presentation.api.api_application import ApiApplication
from src.presentation.exceptions import PresentationException


async def run() -> None:
    settings_path = os.getenv("SETTINGS", "build/settings")
    if settings_path is None:
        raise PresentationException("Settings environment not specified")
    app = await ApiApplication.from_config(settings_path)

    try:
        await app.run()
    finally:
        await app.shutdown()


def main() -> None:
    try:
        asyncio.run(run())
        exit(1)
    except (SystemExit, KeyboardInterrupt):
        exit(1)


if __name__ == "__main__":
    main()
