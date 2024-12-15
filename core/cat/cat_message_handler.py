from dataclasses import dataclass

import httpx

from core.message import Message
from shared.logger import Logger
from shared.message_bus import MessageHandler
from shared.message_sender import MessageSender, Message as Body


@dataclass(frozen=True)
class CatMessage(Message):
    """
    Implementation of the Message class for cat messages.
    """

    @staticmethod
    def id() -> str:
        return 'cat_message'


class CatMessageHandler(MessageHandler):
    """
    Handler class implementation for handling cat messages
    """

    def __init__(
            self,
            logger: Logger,
            sender: MessageSender,
    ):
        self.logger = logger
        self.sender = sender

    async def handle(self, message: CatMessage) -> None:
        cat = await self.__fetch_cat()
        message_to_send = {
            'message': f"{cat}",
            'extra_args': {
                'chat_id': message.chat_id,
                'thread_id': message.thread_id
            }
        }

        writer = message.sender_or_fail()
        self.logger.info("User requested an cat", user_id=writer.id, username=writer.username)
        await self.sender.send(message=Body(**message_to_send))

    async def __fetch_cat(self) -> str:
        async with httpx.AsyncClient() as client:
            response = await client.get(url='https://api.thecatapi.com/v1/images/search', )
            return response.json()[0]['url']

