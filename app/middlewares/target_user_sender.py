import logging
import utils

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import current_handler, CancelHandler

from typing import Callable, Coroutine

from aiogram import types
from pyrogram import Client


def target_user_required(handler: Callable[[types.Message, int], Coroutine]):
    """
    Makes handler
    :param handler:
    :return:
    """
    setattr(handler, "target_user_required", True)
    return handler


class TargetUserSender(BaseMiddleware):
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
        if handler of this message requires target_user, will send the user_id to handler
        if not, does nothing
        :param message: A message
        :param data: A data from another middleware
        :return: None
        """

        handler = current_handler.get()

        if not hasattr(handler, 'target_user_required') or not getattr(handler, "target_user_required"):
            # if handler don't require target-user's id, all is ok, skip update
            return

        # firstly try to get username from args
        args = utils.message.get_arguments(message)

        logging.debug(f"'{handler}' required target-user's id")
        logging.debug(f"Arguments of message: {args}")

        logging.debug(
            f"Message which was replied: {message.reply_to_message.message_id if message.reply_to_message else None}"
        )

        if args:
            logging.debug("Trying to get user's id from provided argument...")
            # get the first argument
            username = args[0]
            try:
                # make call to MT-PROTO-API
                user = await self.pyrogram_client.get_users(username.removeprefix("@"))
            except Exception as e:
                logging.error(f"Error occurred during getting the user with MT-PROTO Api, {e}")
                await message.reply(f"An error occurred during getting this user, check username or try later...")
                raise CancelHandler

            data["target_user_id"] = user.id
            logging.debug("OK! User obtained.")
        elif message.reply_to_message:
            # if arguments not provided, but message is reply to another message
            # we give id from message which was replied
            logging.debug("Getting a user-id from replied message")
            data["target_user_id"] = message.reply_to_message.from_user.id
        else:
            logging.debug("Invalid message received, raising CancelHandler()")
            await message.reply("Please, provide a username or send your message as reply!")
            raise CancelHandler
