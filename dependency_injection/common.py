from kink import di, Container
from telethon import TelegramClient

from config import Config
from config.administrators import InMemoryAdministratorsStorage
from shared.environment_var_getter import OSEnvironmentVarGetter, EnvironmentVarGetter
from shared.logger import JsonStructuredLogger, Logger
from shared.message_bus import AwaitableMessageBus, MessageBus
from shared.telethon_utils import create_bot_telegram_client


async def common_services_bootstrap_di() -> None:
    """
    Populates the kink Container named 'di' with instances of:
        - Config
        - EnvironmentVarGetter
        - Logger
        - InMemoryAdministratorsStorage
        - MessageBus
        - TelegramClient
    :return:
    """
    di[EnvironmentVarGetter] = OSEnvironmentVarGetter()
    di[Config] = Config.from_yaml(
        env=di[EnvironmentVarGetter].get_or_fail('APP_ENV'),
        config_file_path='./config/config.yaml'
    )
    di[Logger] = JsonStructuredLogger()
    di[InMemoryAdministratorsStorage] = InMemoryAdministratorsStorage()
    di[MessageBus] = AwaitableMessageBus(logger=di[Logger])
    di[TelegramClient] = None

    if di[Config].environment.is_testing():
        await __init_common_services_testing(di)


async def __init_common_services_testing(container: Container) -> None:
    """
    Initiates a Telegram Client for working against our bot for testing purposes.
    This client is also stored in the kink Container
    :param container: the kink Container
    """
    env = container[EnvironmentVarGetter]
    app_id, app_hash = (
        env.get_or_fail('TELEGRAM_APP_ID'),
        env.get_or_fail('TELEGRAM_APP_HASH'),
    )

    container[TelegramClient] = create_bot_telegram_client(
        app_id=int(app_id),
        app_hash=app_hash,
    )
