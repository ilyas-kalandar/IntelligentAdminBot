from datetime import datetime

from aiogram import types, Dispatcher

from core import register_handler_with_base_filters
from dispatcher import user_bot


async def status(message: types.Message):
    """
    Represents an information about chat
    :param message: A telegram message
    :return: None
    """

    first_message = await user_bot.get_message(message.chat.id, 1)
    creation_time = datetime.fromtimestamp(first_message.date)
    members_count = await message.bot.get_chat_members_count(message.chat.id)

    result = f"<b>Chat information</b> ℹ \n" \
             f"<b>Chat name</b>: {message.chat.full_name}\n" \
             f"<b>Members count</b> 🙋‍: {members_count}\n" \
             f"<b>Total messages</b> 📉: {message.message_id}\n" \
             f"<b>Chat ID</b> 🛠: <code>{message.chat.id}</code> \n" \
             f"<b>Creation time</b> 📅: {creation_time}"

    await message.reply(result)


async def delete_if_ro(message: types.Message):
    """
    Delete message if Read-Only mode enabled.
    :param message: A telegram message
    """
    await message.delete()


def register_user_handlers(dp: Dispatcher):
    """
    Registers handlers for user messages.
    :param dp: A dispatcher
    """
    register_handler_with_base_filters(dp, status, commands=['stat', 'status'])
    dp.register_message_handler(delete_if_ro, is_admin=False, read_only=True)
