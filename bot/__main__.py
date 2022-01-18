import dispatcher
from constants import BOT_VERSION
from aiogram.utils import executor
from aiogram import Dispatcher
from loguru import logger


def load_filters(dp: Dispatcher):
    """Loads filters"""
    pass


def load_handlers(dp: Dispatcher):
    """Loads handlers"""
    pass


async def on_startup(dp: Dispatcher):
    logger.info("on_startup started")
    logger.info("Loading filters...")
    load_filters(dp)
    logger.success("Filters loaded.")
    logger.info("Loading handlers...")
    logger.success("Handlers loaded.")

    logger.info("All is ready, starting messages dispatching...")


def main():
    executor.start_polling(
        dispatcher.dispatcher,
        skip_updates=True,
        on_startup=on_startup
    )


if __name__ == '__main__':
    logger.info(f"Starting Intelligent Bot ver {BOT_VERSION}")
    main()
