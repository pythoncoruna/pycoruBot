from dataclasses import dataclass

from config.administrators import InMemoryAdministratorsStorage
from core.message import Message
from shared.logger import Logger
from shared.message_bus import MessageHandler
from shared.message_sender import MessageSender, Message as Body

GENERAL_MENU = """
Commandos actualmente habilitados en el bot:
/help - Listado de comandos habilitados
"""

@dataclass(frozen=True)
class HelpMessage(Message):
    """
    Implementation of the Message class for help messages.
    """

    @staticmethod
    def id() -> str:
        return 'help_message'


class HelpMessageHandler(MessageHandler):
    """
    Handler class implementation for handling help messages
    """

    def __init__(
            self,
            logger: Logger,
            admins_repo: InMemoryAdministratorsStorage,
            sender: MessageSender,
    ):
        self.logger = logger
        self.admins_repo = admins_repo
        self.sender = sender

    async def handle(self, message: HelpMessage) -> None:
        writer = message.sender_or_fail()
        writer_is_admin = self.admins_repo.exists_by_handle(writer.username)

        message_to_send = {
            'message': f"{GENERAL_MENU}",
            'extra_args': {
                'chat_id': message.chat_id,
                'thread_id': message.thread_id
            }
        }

        if writer_is_admin:
            self.logger.info("Admin help requested", user_id=writer.id, username=writer.username)
            await self.sender.send(message=Body(**message_to_send))
            return

        self.logger.info("User help requested", user_id=writer.id, username=writer.username)
        await self.sender.send(message=Body(**message_to_send))
