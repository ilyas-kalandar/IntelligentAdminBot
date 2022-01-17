from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from bot import built_vars


class IsReadOnly(BoundFilter):
    """
    Filter that checks for read-only mode enabled
    """
    key = 'read_only'

    def __init__(self, read_only: bool):
        self.read_only = read_only

    async def check(self, message: types.Message):
        return self.read_only == built_vars.read_only[message.chat.id]