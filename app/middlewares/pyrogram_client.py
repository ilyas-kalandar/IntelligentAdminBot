import logging

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import current_handler

from typing import Callable, Coroutine

from aiogram import types
from pyrogram import Client


def pyrogram_client_required(handler: Callable[[types.Message, int], Coroutine]):
    """
    Marks handler for sending pyrogram_client
    :param handler: Message handler
    :rtype: Callable[[types.Message, int], Coroutine]
    :return: A handler
    """
    setattr(handler, "pyrogram_client_required", True)
    return handler


class PyrogramClientMiddleware(BaseMiddleware):
    """
    Middleware for sending target-user's id to handlers
    """

    def __init__(self, pyrogram_client: Client):
        """
        Initializes self
        :param pyrogram_client: An initialized pyrogram client
        """

        self.pyrogram_client = pyrogram_client

        super().__init__()

    async def on_process_message(self, message: types.Message, data: dict):
        """
        Method for preprocessing messages
        if handler of this message requires pyrogram-client, will send the client to handler
        if not, does nothing
        :param message: A message
        :param data: A data from another middleware
        :return: None
        """

        handler = current_handler.get()

        if not hasattr(handler, 'pyrogram_client_required') or not getattr(handler, "pyrogram_client_required"):
            # if handler don't require pyrogram-client, all is ok
            return

        logging.debug(f"{handler} required pyrogram-client, sending...")

        data["pyrogram_client"] = self.pyrogram_client
