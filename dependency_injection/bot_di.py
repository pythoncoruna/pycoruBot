from kink import di
from telegram.ext import CommandHandler, ApplicationBuilder, Application as TelegramBot

from config import Config
from core.help.help_telegram_message_handler import new_wrapped_help_message_handler
from core.insult.insult_telegram_message_handler import new_wrapped_insult_message_handler
from shared.environment_var_getter import EnvironmentVarGetter
from shared.message_bus import MessageBus
from shared.message_sender import MessageSender, TelegramMessageSender
from shared.telegram_utils import TelegramHandlers


async def build_telegram_bot_instance(
        env_getter: EnvironmentVarGetter,
        config: Config,
        handlers: TelegramHandlers,
) -> TelegramBot:
    """
    Builds the main Telegram bot reference with config values
    :param env_getter: the object for getting environment values
    :param config: the configuration instance
    :param handlers: the telegram handlers for each use case
    :return: the bot reference
    """
    token = env_getter.get_or_fail('BOT_TOKEN')

    telegram_bot = ApplicationBuilder() \
        .token(token) \
        .read_timeout(config.telegram.telegram_read_timeout_seconds) \
        .write_timeout(config.telegram.telegram_write_timeout_seconds) \
        .build()

    for command, handler in handlers.items():
        telegram_bot.add_handler(CommandHandler(command=command, callback=handler))

    return telegram_bot


async def bot_bootstrap_di() -> None:
    """
    Defines handlers for different kinds of messages
    """
    help_cmd_handler = new_wrapped_help_message_handler(message_bus=di[MessageBus])
    insult_cmd_handler = new_wrapped_insult_message_handler(message_bus=di[MessageBus])
    di[TelegramBot] = await build_telegram_bot_instance(
        env_getter=di[EnvironmentVarGetter],
        config=di[Config],
        handlers={
            'help': help_cmd_handler,
            'insult': insult_cmd_handler,
        }
    )

    di[MessageSender] = TelegramMessageSender(application=di[TelegramBot])
