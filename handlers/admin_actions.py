from aiogram import Dispatcher, types

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
    command = message.get_command(True).lower()

    await message.bot.kick_chat_member(message.chat.id, user_id)
    await message.reply(
        f"You {'banned' if command != 'ban' else 'kicked'}{mention_user(full_name, user_id)}"
    )

    if command == 'kick':
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
        f"You unbanned {mention_user(full_name, user_id)}"
    )


def register_admin_actions(dp_instance: Dispatcher):
    """
    Register handlers for administrative actions
    :param dp_instance: A dispatcher instance
    :return:
    """
    dp_instance.register_message_handler(cmd_ban, commands=['ban', 'kick'], chat_id=CHAT_ID, can_restrict_members=True,
                                         commands_prefix='!/')
    dp_instance.register_message_handler(cmd_unban, commands=['unban'], chat_id=CHAT_ID, can_restrict_members=True,
                                         commands_prefix='!/')
