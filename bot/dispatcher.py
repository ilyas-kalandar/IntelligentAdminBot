from aiogram import Dispatcher, Bot
from config import CONFIG

BOT = Bot(CONFIG.BOT.TOKEN)
DISPATCHER = Dispatcher(BOT)
