from loguru import logger

from bot.configurator import Configuration

from aiogram.utils import executor
from aiogram import Bot, Dispatcher

import filters
import handlers


async def on_startup(dp: Dispatcher):
    """
    Function which will be called after bot startup
    :param dp: A dispatcher
    """

    logger.info("on_startup running")

    filters.setup_filters(dp)
    logger.success("Filters ready")
    handlers.setup_handlers(dp)
    logger.success("Handlers ready")

    # add tasks here


def run(config: Configuration):
    """
    Runs the bot
    :param config: A configuration-object
    """

    bot = Bot(config.bot_token, parse_mode='html')
    dispatcher_instance = Dispatcher(bot)

    executor.start_polling(dispatcher=dispatcher_instance)
