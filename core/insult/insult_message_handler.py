from dataclasses import dataclass

import httpx

from core.message import Message
from shared.logger import Logger
from shared.message_bus import MessageHandler
from shared.message_sender import MessageSender, Message as Body


@dataclass(frozen=True)
class InsultMessage(Message):
    """
    Implementation of the Message class for insult messages.
    """

    @staticmethod
    def id() -> str:
        return 'insult_message'


class InsultMessageHandler(MessageHandler):
    """
    Handler class implementation for handling insult messages
    """

    def __init__(
            self,
            logger: Logger,
            sender: MessageSender,
    ):
        self.logger = logger
        self.sender = sender

    async def handle(self, message: InsultMessage) -> None:
        insult = await self.__fetch_insult()
        message_to_send = {
            'message': f"{insult}",
            'extra_args': {
                'chat_id': message.chat_id,
                'thread_id': message.thread_id
            }
        }

        writer = message.sender_or_fail()
        self.logger.info("User requested an insult", user_id=writer.id, username=writer.username)
        await self.sender.send(message=Body(**message_to_send))

    async def __fetch_insult(self) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url='https://evilinsult.com/generate_insult.php', params={'lang':'es', 'type':'text'})
            return response.text

