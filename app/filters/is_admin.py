from aiogram.dispatcher.filters import BoundFilter
from aiogram import types
from typing import Union


class IsAdmin(BoundFilter):
    """
    Filter for checking user for having administrative status
    """

    key = "is_admin"

    def __init__(self, is_admin: bool):
        """
        Initializes self
        :param is_admin:Is admin?
        """
        self.is_admin = is_admin

    async def check(self, message: Union[types.Message, types.CallbackQuery]):
        """
        Checks the user rights, if user is admin, returns True
        if not, returns False
        :param message: A message
        """

        if isinstance(message, types.Message):
            member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        else:
            member = await message.bot.get_chat_member(message.message.chat.id, message.from_user.id)

        return self.is_admin is member.is_chat_admin()
