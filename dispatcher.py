from aiogram import Bot, Dispatcher

from filters import IsAdminFilter, CanRestrictMembers, ReadOnlyFilter
from userbot import UserBot
from built_vars import CONFIG

# bot

bot = Bot(CONFIG.get_param("bot", "Token"), parse_mode='html')
dp = Dispatcher(bot)

# user bot
user_bot = UserBot(CONFIG.get_param("Pyrogram", "ApiHash"), CONFIG.get_param("Pyrogram", "ApiID"))

# register filters
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(CanRestrictMembers)
dp.filters_factory.bind(ReadOnlyFilter)
