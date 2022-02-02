from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from configurator import BotConfig
from aiogram import types

import logging


class SkipUpdateMiddleware(BaseMiddleware):
    """Middleware for skipping not needed updates"""

    def __init__(self, config: BotConfig):
        """
        Initializes self
        :param config:
        """
        super().__init__()
        self.config = config

    async def on_pre_process_message(self, message: types.Message, data: dict):
        if message.chat.id not in self.config.served_chats:
            # if we don't do serving update's chat's id, skip it
            logging.info(f"{message.chat.id} not in served_chats list, skipping update.")
            raise CancelHandler()

        # handle update
