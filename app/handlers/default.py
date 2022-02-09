from aiogram import Dispatcher, types

from middlewares import pyrogram_client_required, target_user_required
from pyrogram import Client
from datetime import datetime
from constants import BOT_VERSION

import logging


@pyrogram_client_required
async def chat_status(message: types.Message, pyrogram_client: Client):
    """
    Represents an information about chat
    :param pyrogram_client: A pyrogram-client
    :param message: A telegram message
    :return: None
    """

    first_message = await pyrogram_client.get_messages(message.chat.id, 1)

    try:
        creation_time = datetime.fromtimestamp(first_message.date)
    except Exception as e:
        logging.error(f"The follow exception occurred during retrieving first message's date '{e}'")
        creation_time = "Unknown"

    members_count = await message.bot.get_chat_members_count(message.chat.id)

    result = f"<b>Chat information</b> ℹ \n" \
             f"<b>Chat name</b>: {message.chat.full_name}\n" \
             f"<b>Members count</b> 🙋‍: {members_count}\n" \
             f"<b>Total messages</b> 📉: {message.message_id}\n" \
             f"<b>Chat ID</b> 🛠: <code>{message.chat.id}</code> \n" \
             f"<b>Creation time</b> 📅: {creation_time}\n\n" \
             f"<b>Bot version</b>: {BOT_VERSION}\n" \
             f"<b>Created by @Awaitable</b>"

    await message.reply(result)


@target_user_required
async def chat_member_info(message: types.Message, target_user_id: int):
    """
    Returns information about concrete chat member
    :param message: A message
    :param target_user_id: An ID of user
    """

    dp = Dispatcher.get_current()
    chat_member = await dp.bot.get_chat_member(message.chat.id, target_user_id)
    data = await dp.storage.get_data(chat=message.chat.id)

    count = data["messages_count"]

    result = "<b>Information about chat-member</b> 🙋: {name}\n\n" \
             "<b>UserID 🛠</b>: <code>{user_id}</code>\n" \
             "<b>Messages count 📉</b>: {msg_count}\n" \
             "<b>Is bot</b>: <code>{is_bot}</code>\n"

    await message.reply(
        result.format(
            name=chat_member.user.mention,
            user_id=chat_member.user.id,
            msg_count=count[chat_member.user.id],
            is_bot=chat_member.user.is_bot
        )
    )


async def help_(message: types.Message):
    """
    Just help menu
    :param message: A message
    :return: None
    """

    text = "<b>Intelligent bot help</b>\n" \
           "/help - <b>Show this</b>\n\n" \
           "Commands such as ban/kick/mute/unban/unmute/info must be provided with argument or sent as <b>reply</b>\n" \
           "/ban - <b>Ban user</b>\n" \
           "/unban - <b>Unban user</b>\n" \
           "/mute - <b>Mute user</b>\n" \
           "/unmute - <b>Unmute user</b>\n" \
           "/kick - <b>Kick user (remove)</b>\n" \
           "/info - <b>Information about user</b>\n" \
           "/stat - <b>Information about group</b>\n" \
           "/top - <b>Get top active-users of chat</b>\n"
    await message.reply(
        text
    )


async def top(message: types.Message):
    """
    Returns a top 10 active users in chat
    :param message: A message
    """

    dp = Dispatcher.get_current()
    data = await dp.storage.get_data(chat=message.chat.id)

    members = data["messages_count"].most_common()[:10]
    cnt = 1
    users_top = []

    for member, msg_count in members:
        chat_member = await message.bot.get_chat_member(message.chat.id, member)
        users_top.append(
            "{cnt}. {user} | {msg_count}".format(
                cnt=cnt,
                user=chat_member.user.full_name,
                msg_count=msg_count
            )
        )
        cnt += 1

    final_message = "Current top\n{}"

    await message.reply(final_message.format(
        "\n".join(users_top)
    ))


def setup_default(dp: Dispatcher):
    """
    Setup's an administrative handlers
    :param dp: A dispatcher
    :return: None
    """

    dp.register_message_handler(chat_status, commands=['stat', 'status'], commands_prefix='!/')
    dp.register_message_handler(chat_member_info, commands=['info'], commands_prefix="!/")
    dp.register_message_handler(top, commands=['top'], commands_prefix="!/")
    dp.register_message_handler(help_, commands=['help'], commands_prefix="!/")
