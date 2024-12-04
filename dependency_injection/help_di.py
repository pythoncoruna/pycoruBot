from kink import di

from config.administrators import InMemoryAdministratorsStorage
from core.help.help_menu_composer import HelpMenuComposer
from core.help.help_message_handler import HelpMessage, HelpMessageHandler
from shared.logger import Logger
from shared.message_bus import MessageBus
from shared.message_sender import MessageSender


async def help_bootstrap_di() -> None:
    """
    Maps the HelpMessage type of message
    with the proper handler for it (HelpMessageHandler) so that
    it will be called when these messages are received
    """
    message_bus, logger, admins_repo, message_sender = (
        di[MessageBus],
        di[Logger],
        di[InMemoryAdministratorsStorage],
        di[MessageSender],
    )

    await message_bus.register_message_handler(
        message=HelpMessage,
        handler=HelpMessageHandler(
            logger=logger,
            admins_repo=admins_repo,
            help_menu_composer=HelpMenuComposer(),
            sender=message_sender
        )
    )
