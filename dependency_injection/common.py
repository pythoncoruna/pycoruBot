from kink import di

from config import Config
from config.administrators import InMemoryAdministratorsStorage
from shared.environment_var_getter import OSEnvironmentVarGetter, EnvironmentVarGetter
from shared.logger import JsonStructuredLogger, Logger
from shared.message_bus import AwaitableMessageBus, MessageBus



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


