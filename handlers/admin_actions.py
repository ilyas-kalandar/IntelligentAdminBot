from aiogram import Dispatcher, types

from dispatcher import bot
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
    await bot.kick_chat_member(message.chat.id, user_id)
    await message.reply(
        f"You banned {mention_user(full_name, user_id)}"
    )


@catch_exceptions
@send_id
async def cmd_unban(message: types.Message, user_id: int, full_name: str):
    """
    Command for unbanning member

    :param message: A telegram message of admin
    :param user_id: A Telegram-ID of user which will be unbanned
    :param full_name: A fullname of user which will be unbanned
    """
    await bot.unban_chat_member(message.chat.id, user_id, only_if_banned=True)
    await message.reply(
        f"You unbanned {mention_user(full_name, user_id)}"
    )


def register_admin_actions(dp_instance: Dispatcher):
    """
    Register handlers for administrative actions
    :param dp_instance: A dispatcher instance
    :return:
    """
    dp_instance.register_message_handler(cmd_ban, commands=['ban'], chat_id=CHAT_ID, can_restrict_members=True,
                                         commands_prefix='!/')
    dp_instance.register_message_handler(cmd_unban, commands=['unban'], chat_id=CHAT_ID, can_restrict_members=True,
                                         commands_prefix='!/')
