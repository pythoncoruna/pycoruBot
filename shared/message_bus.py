from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Text, Type, TypeVar, Optional

from shared.logger import Logger

Result = TypeVar('Result')


@dataclass(frozen=True)
class Dto(ABC):
    @staticmethod
    @abstractmethod
    def id() -> str:
        pass


class InvalidDto(Exception):
    """
    Exception raised when an invalid Dto is passed.
    """

    def __init__(self, message: str):
        self.message = message


class MessageHandler(ABC):
    """
    Abstract class for message handlers.
    """
    @abstractmethod
    def handle(self, message: Dto) -> Optional[Result]:
        pass


class MessageBus(ABC):
    """
    Abstract class for defining how to map handlers to message types
    """
    @abstractmethod
    async def register_message_handler(self, message_type: Type[Dto], handler: MessageHandler) -> None:
        """
        Register a handler to a specific message type
        :param message_type: the kind of message type to register for the handler
        :param handler: the handler that will process the messages
        :return:
        """
        pass

    @abstractmethod
    async def handle(self, message: Dto) -> Optional[Result]:
        """
        Handles a message
        :param message: the message
        :return: the result
        """
        pass


class AwaitableMessageBus(MessageBus):
    """
    Implementation class for defining how to map handlers to message types
    """

    def __init__(self, logger: Logger):
        self.logger = logger
        self.handlers: Dict[Text, MessageHandler] = dict()

    async def register_message_handler(self, message_type: Type[Dto], handler: MessageHandler) -> None:
        message_name = message_type.id()

        if message_name in self.handlers:
            raise InvalidDto('Command <%s> already registered' % message_name)

        self.handlers[message_name] = handler

    async def handle(self, message: Dto) -> Optional[Result]:
        message_name = message.id()
        if message_name in self.handlers:
            handler = self.handlers[message_name]
            self.logger.info(f'Handling message <{handler.__class__}:{message_name}>')

            return await handler.handle(message)

        raise InvalidDto('Command <%s> not registered' % message_name)
