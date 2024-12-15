from kink import di
from telegram.ext import CommandHandler, ApplicationBuilder, Application as TelegramBot

from cat.cat_message_handler import CatMessage
from config import Config
from help.help_message_handler import HelpMessage
from insult.insult_message_handler import InsultMessage
from shared.environment_var_getter import EnvironmentVarGetter
from shared.message_bus import MessageBus
from shared.message_sender import MessageSender, TelegramMessageSender
from shared.telegram_utils import TelegramHandlers
from telegram_message_handler import new_wrapped_message_handler


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
    mappings = {
        'help': HelpMessage,
        'insult': InsultMessage,
        'cat': CatMessage,
    }

    handlers_dict = { command: new_wrapped_message_handler(message_bus=di[MessageBus], message_type_class=mtype)
          for command,mtype in mappings.items()
    }

    di[TelegramBot] = await build_telegram_bot_instance(
        env_getter=di[EnvironmentVarGetter],
        config=di[Config],
        handlers=handlers_dict
    )

    di[MessageSender] = TelegramMessageSender(application=di[TelegramBot])
