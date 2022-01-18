from aiogram import Dispatcher, Bot
from config import CONFIG

bot = Bot(CONFIG.bot.TOKEN)
dispatcher = Dispatcher(bot)
