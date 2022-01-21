import logging
import configurator

from argparse import ArgumentParser
from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from constants import BOT_VERSION

logger = logging.getLogger(__name__)


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
    logger.info("Filters loaded.")
    logger.info("Loading handlers...")
    load_handlers(dp)
    logger.info("Handlers loaded.")
    logger.info("All is ready, starting messages dispatching...")


def build_parser() -> ArgumentParser:
    """
    Builds an instance of command-line arguments parser
    :return: An Parser instance
    """
    parser = ArgumentParser()
    parser.add_argument("--config", description="File with configuration", default=None)
    parser.add_argument("--logs-level", default="info", description="Logging level (info or debug)")

    return parser


def main():
    """Heart of project"""

    parser = build_parser()
    args = parser.parse_args()

    if args.config.endswith(".ini"):
        config = configurator.load_from_ini(args.config)
    elif args.config.endswith(".env"):
        config = configurator.load_from_dotenv(args.config)
    else:
        config = configurator.load_from_environ()

    level = logging.INFO

    if config.bot.debug:
        level = logging.DEBUG

    logging.basicConfig(level=level)

    bot = Bot(config.bot.token)
    dispatcher = Dispatcher(bot)

    executor.start_polling(
        dispatcher=dispatcher,
        skip_updates=True,
        on_startup=on_startup
    )


if __name__ == '__main__':
    logger.info(f"Starting Intelligent Bot ver {BOT_VERSION}")
    main()
