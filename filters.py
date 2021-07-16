from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

import built_vars
from settings import CHAT_ID


class IsAdminFilter(BoundFilter):
    """
    Filter that checks admin rights existence
    """
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: types.Message) -> bool:
        member = await message.bot.get_chat_member(CHAT_ID, message.from_user.id)
        return self.is_admin == member.is_chat_admin()


class CanRestrictMembers(BoundFilter):
    """
    Filter that checks member ability for restricting
    """
    key = 'can_restrict_members'

    def __init__(self, can_restrict_members: bool):
        self.can_restrict_members = can_restrict_members

    async def check(self, message: types.Message) -> bool:
        member = await message.bot.get_chat_member(CHAT_ID, message.from_user.id)
        return self.can_restrict_members == member.can_restrict_members or member.is_chat_creator()


class ReadOnlyFilter(BoundFilter):
    """
    Filter that checks for read-only mode enabled
    """
    key = 'read_only'

    def __init__(self, read_only):
        self.read_only = read_only

    async def check(self, message):
        print(built_vars.READ_ONLY)
        return self.read_only == built_vars.READ_ONLY
