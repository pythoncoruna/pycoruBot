from kink import di

from core.insult.insult_message_handler import InsultMessage, InsultMessageHandler
from shared.logger import Logger
from shared.message_bus import MessageBus
from shared.message_sender import MessageSender


async def insult_bootstrap_di() -> None:
    """
    Maps the InsultMessage type of message
    with the proper handler for it (InsultMessageHandler) so that
    it will be called when these messages are received
    """
    message_bus, logger, message_sender = (
        di[MessageBus],
        di[Logger],
        di[MessageSender],
    )

    await message_bus.register_message_handler(
        message_type=InsultMessage,
        handler=InsultMessageHandler(
            logger=logger,
            sender=message_sender
        )
    )
