from datetime import datetime

from aiogram import types, Dispatcher

from dispatcher import user_bot
from settings import CHAT_ID


async def status(message: types.Message):
    """
    Represents an information about chat
    :param message: A telegram message
    :return: None
    """
    first_message = await user_bot.get_message(message.chat.id, 1)
    creation_time = datetime.fromtimestamp(first_message.date)
    members_count = await message.bot.get_chat_members_count(message.chat.id)

    result = "<b>Chat information</b> ℹ \n" + \
             f"<b>Chat name</b>: {message.chat.full_name}\n" + \
             f"<b>Members count</b> 🙋‍: {members_count}\n" + \
             f"<b>Total messages</b> 📉: {message.message_id}\n" + \
             f"<b>Chat ID</b> 🛠: <code>{message.chat.id}</code> \n" + \
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
    dp.register_message_handler(status, commands=['stat', 'status'], chat_id=CHAT_ID, commands_prefix='!/')
    dp.register_message_handler(delete_if_ro, is_admin=False, read_only=True)
