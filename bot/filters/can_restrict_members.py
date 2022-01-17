from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class CanRestrictMembers(BoundFilter):
    """
    Filter that checks member ability for restricting
    """
    key = 'can_restrict_members'

    def __init__(self, can_restrict_members: bool):
        self.can_restrict_members = can_restrict_members

    async def check(self, message: types.Message) -> bool:
        member = await message.bot.get_chat_member(message.chat.id, message.from_user.id)
        return (member.is_chat_creator() or member.can_restrict_members) == self.can_restrict_members