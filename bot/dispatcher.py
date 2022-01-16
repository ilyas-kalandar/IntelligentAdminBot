from aiogram import Bot, Dispatcher

from filters import IsAdminFilter, CanRestrictMembers, ReadOnlyFilter
from bot.userbot import UserBot
from bot.built_vars import config

# bot

bot = Bot(config.bot.token, parse_mode='html')
dp = Dispatcher(bot)

# user bot
user_bot = UserBot(config.pyrogram.api_hash, config.pyrogram.api_id)

# register filters
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(CanRestrictMembers)
dp.filters_factory.bind(ReadOnlyFilter)
