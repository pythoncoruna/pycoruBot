from kink import di

from core.cat.cat_message_handler import CatMessage, CatMessageHandler
from shared.logger import Logger
from shared.message_bus import MessageBus
from shared.message_sender import MessageSender


async def cat_bootstrap_di() -> None:
    """
    Maps the CatMessage type of message
    with the proper handler for it (CatMessageHandler) so that
    it will be called when these messages are received
    """
    message_bus, logger, message_sender = (
        di[MessageBus],
        di[Logger],
        di[MessageSender],
    )

    await message_bus.register_message_handler(
        message_type=CatMessage,
        handler=CatMessageHandler(
            logger=logger,
            sender=message_sender
        )
    )
