from aiogram import Bot, Dispatcher

import settings
from filters import IsAdminFilter, CanRestrictMembers
from userbot import UserBot

# bot

bot = Bot(settings.BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot)

# user bot
user_bot = UserBot(settings.API_HASH, settings.API_ID)

# register filters
dp.filters_factory.bind(IsAdminFilter)
dp.filters_factory.bind(CanRestrictMembers)
