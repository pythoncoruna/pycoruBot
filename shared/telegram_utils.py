import os
from typing import Callable, Dict, Text, Coroutine, Tuple, Optional, Any

from kink import di
from telegram import Update
from telegram.ext import Application, CallbackContext

from core.message import User
from shared.message_sender import MessageSender

TelegramHandler = Callable[[Update, CallbackContext], Coroutine[Any, Any, None]]
TelegramHandlers = Dict[Text, TelegramHandler]


class TelegramUpdateError(Exception):
    """
    Exception for raising when a Telegram Update causes some error
    """
    @classmethod
    def update_without_from_user(cls) -> 'TelegramUpdateError':
        return cls('Update received without user')


async def sender_from_message_update(update: Update) -> User:
    """
    Creates a User instance out of a Telegram update
    :param update: the Telegram update
    :return: the already built User
    """
    if update.message and update.message.from_user:
        return User(**{
            'id': update.message.from_user.id,
            'first_name': update.message.from_user.first_name,
            'last_name': update.message.from_user.last_name,
            'username': update.message.from_user.username,
            'language_iso2': update.message.from_user.language_code,
            'is_bot': update.message.from_user.is_bot,
        })

    raise TelegramUpdateError.update_without_from_user()


async def message_content_from_update_or_fail(update: Update) -> Tuple[int, Optional[Text], Optional[int]]:
    if update.message:
        return update.message.chat_id, update.message.text, update.message.message_thread_id

    raise TelegramUpdateError.update_without_from_user()


async def init_bot(bot: Application) -> None:
    """
    Initiates the bot application
    :param bot: the bot reference
    """
    await bot.initialize()
    await bot.start()
    await bot.updater.start_polling(allowed_updates=Update.ALL_TYPES)

async def announce_available(bot: Application) -> None:
    sender = di[MessageSender]
    await sender.application.bot.send_message(text="I'm available!", chat_id=os.environ.get('DEV_TG_CHAT_ID'))

async def shutdown_bot(bot: Application) -> None:
    """
    Shuts down the bot
    :param bot: the bot reference
    """
    if bot.updater.running:
        await bot.updater.stop()

    if bot.running:
        await bot.stop()
        await bot.shutdown()
