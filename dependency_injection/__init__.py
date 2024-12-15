from pathlib import Path
from typing import Text

from dotenv import load_dotenv
from kink import Container, di

from cat_di import cat_bootstrap_di
from dependency_injection.bot_di import bot_bootstrap_di
from dependency_injection.common import common_services_bootstrap_di
from dependency_injection.help_di import help_bootstrap_di
from dependency_injection.insult_di import insult_bootstrap_di


async def bootstrap_di() -> Container:
    """
    Creates the kink global Container, populates it and returns it
    :return: the kink Container instance
    """
    load_dotenv(dotenv_path=Path('.env'), override=True)

    await common_services_bootstrap_di()
    # Creates handlers for different kinds of messages
    await bot_bootstrap_di()

    # These functions map a message_type to a specific handler
    await help_bootstrap_di()
    await insult_bootstrap_di()
    await cat_bootstrap_di()
    return di


async def bootstrap_di_with_env_files(*args: Text) -> Container:
    """
    Returns a kink global container. Same as bootstrap_di()
    but with a custom env file or files
    :param args: string iterable with .env filenames
    :return: the kink Container instance
    """
    for path in args:
        load_dotenv(dotenv_path=Path(path), override=True)

    return await bootstrap_di()
