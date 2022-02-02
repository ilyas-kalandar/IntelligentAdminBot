from aiogram import types, Dispatcher
from random import randint

import utils
import keyboards
import logging


async def check_and_ban(captcha_message: types.Message, user_id: int):
    """
    Checks chat-member for ability to sending messages, if it hasn't ability, will ban it
    :param captcha_message: Just message with captcha
    :param user_id:A user_id of user which will be checked
    :return: None
    """

    member = await captcha_message.chat.get_member(user_id)

    try:
        await captcha_message.delete()
    except Exception as e:
        logging.error(f"The following exception was occur while deleting the captcha {e}")

    if not isinstance(member, types.ChatMemberRestricted):
        # ChatMember may be banned, promoted, etc... all is ok
        return

    if member.can_send_messages:
        #  if member can send messages, no problem
        return

    # oh, member can't send messages, because it is fucking bot, let's ban it!

    await captcha_message.bot.ban_chat_member(
        captcha_message.chat.id,
        user_id
    )

    notice = await captcha_message.bot.send_message(
        captcha_message.chat.id,
        "User {} didn't pass the captcha and was banned, so, where is my sirnik?".format(
            utils.message.make_link(str(user_id), user_id)
        )
    )

    utils.asyncio.call_after(notice.delete, 20)


async def captcha(message: types.Message):
    """
    Handler for making captcha
    :param message: A handler
    :return:
    """

    members = message.new_chat_members
    await message.delete()

    for member in members:
        if member.is_bot:
            # if member is Telegram-bot, ok, skip
            continue

        await message.bot.restrict_chat_member(
            message.chat.id,
            member.id,
            can_send_messages=False
        )

        first_value = randint(1, 9)
        second_value = randint(1, 9)

        keyboard = keyboards.reply.gen_captcha_keyboard(
            message.from_user.id,
            first_value + second_value
        )

        captcha_msg = await message.bot.send_message(
            message.chat.id,
            "Hello, {name}!\n{first} + {second} is?".format(
                name=utils.message.make_link(member.full_name, member.id),
                first=first_value,
                second=second_value
            ),
            reply_markup=keyboard
        )

        utils.asyncio.call_after(check_and_ban, 20, captcha_msg, member.id)


def setup_captcha(dp: Dispatcher):
    """
    Setup's captcha to dispatcher
    :param dp: A dispatcher
    :return: None
    """
    dp.register_message_handler(captcha, content_types=["new_chat_members"], is_admin=False)
