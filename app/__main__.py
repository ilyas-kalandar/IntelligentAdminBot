import logging

from pyrogram import Client

import configurator

from argparse import ArgumentParser
from aiogram import Dispatcher, Bot
from aiogram.utils import executor

from constants import BOT_VERSION
from middlewares import TargetUserMiddleware

import handlers

logger = logging.getLogger(__name__)


def client_factory(config: configurator.UserBotConfig) -> Client:
    """
    Returns an initialized client
    :param config: A UserBot configuration
    :return: Pyrogram Client
    """
    client = Client(
        api_hash=config.api_hash,
        api_id=config.api_id,
        session_name="pyrogram",
    )

    client.start()

    return client


def load_filters(dp: Dispatcher):
    """Loads filters"""
    # dp.filters_factory.bind(TargetUserRequired)


def load_handlers(dp: Dispatcher):
    """Loads handlers"""
    handlers.setup(dp)


def build_parser() -> ArgumentParser:
    """
    Builds an instance of command-line arguments parser
    :return: An Parser instance
    """
    parser = ArgumentParser()
    parser.add_argument("--config", help="File with configuration", default="")
    parser.add_argument("--logs-level", default="info", help="Logging level (info or debug)")

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

    logging.info(f"Intelligent Bot, version {BOT_VERSION}")

    bot = Bot(config.bot.token, parse_mode='html')
    dispatcher = Dispatcher(bot)
    client = client_factory(config.userbot)

    # setup middlewares
    logging.info("Loading middlewares...")
    dispatcher.setup_middleware(
        TargetUserMiddleware(client)
    )

    # setup filters
    logging.info("Loading filters...")
    load_filters(dispatcher)

    # setup handlers
    logging.info("Loading handlers...")
    load_handlers(dispatcher)

    executor.start_polling(
        dispatcher=dispatcher,
        skip_updates=True,
    )


if __name__ == '__main__':
    main()
