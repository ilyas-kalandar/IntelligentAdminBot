from aiogram import Dispatcher, types

import built_vars
from settings import CHAT_ID
from utils import mention_user
from .core import send_id, catch_exceptions


@catch_exceptions
@send_id
async def cmd_ban(message: types.Message, user_id: int, full_name: str):
    """
    Command for banning member

    :param message: A telegram message of admin
    :param user_id: A Telegram-ID of user which will be banned
    :param full_name: A fullname of user which will be banned
    """
    command = message.text.lower().split()[0]
    
    await message.bot.kick_chat_member(message.chat.id, user_id)
    await message.reply(
        f"You <b>{'banned' if 'ban' in command else 'kicked'}</b> {mention_user(full_name, user_id)}"
    )

    if 'kick' in command:
        # if user has been kicked, remove him from blacklist
        await message.bot.unban_chat_member(message.chat.id,
                                            user_id)


@catch_exceptions
@send_id
async def cmd_unban(message: types.Message, user_id: int, full_name: str):
    """
    Command for unbanning member

    :param message: A telegram message of admin
    :param user_id: A Telegram-ID of user which will be unbanned
    :param full_name: A fullname of user which will be unbanned
    """
    await message.bot.unban_chat_member(message.chat.id, user_id, only_if_banned=True)
    await message.reply(
        f"You <b>unbanned</b> {mention_user(full_name, user_id)}"
    )


@catch_exceptions
@send_id
async def cmd_mute(message: types.Message, user_id: int, full_name: str):
    """
    Command for muting member

    :param message: A telegram message of admin
    :param user_id: A Telegram-ID of user which will be muted
    :param full_name: A fullname of user which will be muted
    """
    await message.bot.restrict_chat_member(
        message.chat.id,
        user_id,
        can_send_messages=False,
    )
    await message.reply(
        f"You <b>muted</b> {mention_user(full_name, user_id)}"
    )


@catch_exceptions
@send_id
async def cmd_unmute(message: types.Message, user_id: int, full_name: str):
    """
    Command for unmuting member

    :param message: A telegram message of admin
    :param user_id: A Telegram-ID of user which will be unmuted
    :param full_name: A fullname of user which will be unmuted
    """
    await message.bot.restrict_chat_member(
        message.chat.id,
        user_id,
        can_send_other_messages=True,
        can_send_media_messages=True,
        can_send_messages=True,
        can_add_web_page_previews=True,
    )
    await message.reply(
        f"You <b>unmuted</b> {mention_user(full_name, user_id)}")


async def read_only(message: types.Message):
    """
    Enabled/Disable Read-Only mode
    :param message: A telegram message
    :return:
    """
    built_vars.READ_ONLY = False if built_vars.READ_ONLY else True
    await message.answer(f"Read-only mode {'enabled' if built_vars.READ_ONLY else 'disabled'}.")


def register_admin_actions(dp_instance: Dispatcher):
    """
    Register handlers for administrative actions
    :param dp_instance: A dispatcher instance
    :return:
    """
    dp_instance.register_message_handler(cmd_ban, commands=['ban', 'kick'],
                                         chat_id=CHAT_ID,
                                         can_restrict_members=True,
                                         commands_prefix='!/')
    dp_instance.register_message_handler(cmd_unban, commands=['unban'],
                                         chat_id=CHAT_ID,
                                         can_restrict_members=True,
                                         commands_prefix='!/')
    dp_instance.register_message_handler(cmd_mute, commands=['mute'],
                                         chat_id=CHAT_ID,
                                         is_admin=True,
                                         commands_prefix='!/')
    dp_instance.register_message_handler(read_only, commands=['ro', 'readonly'],
                                         chat_id=CHAT_ID,
                                         is_admin=True,
                                         commands_prefix='!/')
    dp_instance.register_message_handler(cmd_unmute, commands=['unmute'],
                                         chat_id=CHAT_ID,
                                         is_admin=True,
                                         commands_prefix='!/')
