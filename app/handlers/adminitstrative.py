from aiogram import types, Dispatcher
from middlewares import target_user_required

import utils


@target_user_required
async def cmd_ban(message: types.Message, target_user_id: int):
    """
    Process the ban command
    :param message: A message from telegram
    :param target_user_id: User-id from user which will be banned
    :return: None
    """
    await message.bot.ban_chat_member(
        message.chat.id,
        target_user_id
    )
    await message.answer(
        "{user} banned {target}".format(
            user=utils.message.make_link(message.from_user.full_name, message.from_user.id),
            target=utils.message.make_link(str(target_user_id), target_user_id)
        )
    )


@target_user_required
async def cmd_unban(message: types.Message, target_user_id: int):
    """
    Process the unban command
    :param message: A message from telegram
    :param target_user_id: User-id from user which will be unbanned
    :return: None
    """
    await message.bot.unban_chat_member(
        message.chat.id,
        target_user_id
    )
    await message.answer(
        "{user} unbanned {target}".format(
            user=utils.message.make_link(message.from_user.full_name, message.from_user.id),
            target=utils.message.make_link(str(target_user_id), target_user_id)
        )
    )


@target_user_required
async def cmd_mute(message: types.Message, target_user_id: int):
    """
    Process the mute command
    :param message: A message from telegram
    :param target_user_id: User-id from user which will be muted
    :return: None
    """
    await message.bot.restrict_chat_member(
        message.chat.id,
        target_user_id,
        can_send_messages=False,
    )
    await message.answer(
        "{user} muted {target}".format(
            user=utils.message.make_link(message.from_user.full_name, message.from_user.id),
            target=utils.message.make_link(str(target_user_id), target_user_id)
        )
    )


@target_user_required
async def cmd_unmute(message: types.Message, target_user_id: int):
    """
    Process the unmute command
    :param message: A message from telegram
    :param target_user_id: User-id from user which will be unmuted
    :return: None
    """
    await message.bot.restrict_chat_member(
        message.chat.id,
        target_user_id,
        can_send_messages=True,
        can_send_media_messages=True,
        can_send_other_messages=True,
        can_add_web_page_previews=True,
    )
    await message.answer(
        "{user} unmuted {target}".format(
            user=utils.message.make_link(message.from_user.full_name, message.from_user.id),
            target=utils.message.make_link(str(target_user_id), target_user_id)
        )
    )


@target_user_required
async def cmd_kick(message: types.Message, target_user_id: int):
    """
    Process the kick command
    :param message: A message from telegram
    :param target_user_id: User-id from user which will be kicked
    :return: None
    """
    await message.bot.kick_chat_member(
        message.chat.id,
        target_user_id
    )
    await message.answer(
        "{user} kicked {target}".format(
            user=utils.message.make_link(message.from_user.full_name, message.from_user.id),
            target=utils.message.make_link(str(target_user_id), target_user_id)
        )
    )


def setup_administrative(dp: Dispatcher):
    """
    Setup's an administrative handlers
    :param dp: A dispatcher
    :return: None
    """

    dp.register_message_handler(
        cmd_ban, commands=['ban'], commands_prefix="!/"
    )
    dp.register_message_handler(
        cmd_unban, commands=['unban'], commands_prefix="!/"
    )
    dp.register_message_handler(
        cmd_mute, commands=['mute'], commands_prefix="!/"
    )
    dp.register_message_handler(
        cmd_unmute, commands=['unmute'], commands_prefix="!/"
    )
    dp.register_message_handler(
        cmd_kick, commands=['kick'], commands_prefix="!/"
    )
