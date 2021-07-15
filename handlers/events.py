from aiogram import Dispatcher
from aiogram.types import Message
from settings import CHAT_ID


async def delete_message(message: Message):
    """
    Delete message :/
    :param message: A message from telegram
    :return:
    """
    await message.delete()  # delete message


def register_event_handlers(dp: Dispatcher):
    dp.register_message_handler(delete_message, chat_id=CHAT_ID, content_types=[
        "new_chat_members",
        "left_chat_member"
    ])
