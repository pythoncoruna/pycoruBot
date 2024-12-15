from typing import Callable, Any, Coroutine

from telegram import Update
from telegram.ext import CallbackContext

from core.cat.cat_message_handler import CatMessage
from shared.message_bus import MessageBus
from shared.telegram_utils import (
    sender_from_message_update,
    message_content_from_update_or_fail
)


def new_wrapped_cat_message_handler(
        message_bus: MessageBus
) -> Callable[[Update, CallbackContext], Coroutine[Any, Any, None]]:
    """
    Creates dynamically the handler for handling specific kinds of messages
    :param message_bus:
    :return:
    """
    async def handler(update: Update, context: CallbackContext):
        sender = await sender_from_message_update(update)
        chat_id, text, thread_id = await message_content_from_update_or_fail(update)
        cat_message = CatMessage(
            user_id=sender.id,
            chat_id=chat_id,
            message=text,
            thread_id=thread_id,
            sender=sender
        )

        await message_bus.handle(cat_message)

    return handler
