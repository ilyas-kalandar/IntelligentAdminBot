import asyncio

from aiogram import Dispatcher
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from dispatcher import bot
from settings import SERVED_CHATS, WAIT_FOR_CAPTCHA_TIME
from utils import mention_user


async def delete_message(message: Message):
    """
    Delete message
    :param message: A message from telegram
    :return:
    """

    await message.delete()  # delete message

    if message.content_type == "new_chat_members":
        # captcha
        keyboard = InlineKeyboardMarkup()
        button = InlineKeyboardButton("I am not robot!",
                                      callback_data=f'captcha {message.from_user.id}')
        keyboard.add(button)

        captcha = await message.answer(
            f"Hello {mention_user(message.from_user.full_name, message.from_user.id)}, are you bot?",
            reply_markup=keyboard,
        )

        await message.bot.restrict_chat_member(
            message.chat.id,
            message.from_user.id,
            can_send_messages=False,
        )

        await asyncio.sleep(WAIT_FOR_CAPTCHA_TIME)

        # obtain member's permissions

        member = await bot.get_chat_member(message.chat.id,
                                           message.from_user.id)

        # if member can't send messages, ban it.

        print(member.can_send_messages)
        print(type(member.can_send_messages))

        # normally, aiogram should return only boolean, but sometimes it returns None instead True

        if member.can_send_messages == False:
            await bot.kick_chat_member(message.chat.id, member.user.id)
            await bot.send_message(message.chat.id,
                                   f"{mention_user(member.user.full_name, member.user.id)} was bot.")

        await captcha.delete()


def register_event_handlers(dp: Dispatcher):
    dp.register_message_handler(delete_message, is_served_chat=True, chat_id=SERVED_CHATS, content_types=[
        "new_chat_members",
        "left_chat_member"
    ])
