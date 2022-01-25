from aiogram import types, Dispatcher
from random import randint

import utils
import keyboards


async def captcha(message: types.Message):
    """
    Handler for making captcha
    :param message:
    :return:
    """
    await message.bot.restrict_chat_member(
        message.chat.id,
        message.from_user.id,
        can_send_messages=False
    )

    await message.delete()

    first_value = randint(1, 9)
    second_value = randint(1, 9)

    keyboard = keyboards.reply.gen_captcha_keyboard(message.from_user.id, first_value + second_value)

    await message.bot.send_message(
        message.chat.id,
        "Hello, {name}!\n{first} + {second} is?".format(
            name=utils.message.make_link(message.from_user.full_name, message.from_user.id),
            first=first_value,
            second=second_value
        ),
        reply_markup=keyboard
    )


def setup_captcha(dp: Dispatcher):
    """
    Setup's captcha to dispatcher
    :param dp: A dispatcher
    :return: None
    """
    dp.register_message_handler(captcha, content_types=["new_chat_members"])
