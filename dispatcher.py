import settings
from aiogram import Bot, Dispatcher

bot = Bot(settings.BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot)
