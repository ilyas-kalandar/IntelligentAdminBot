import logging
import configurator

import handlers
import filters
import utils
import jobs

from pyrogram import Client

from argparse import ArgumentParser
from aiogram import Dispatcher, Bot
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from constants import BOT_VERSION
from middlewares import TargetUserMiddleware, SkipUpdateMiddleware, PyrogramClientMiddleware

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


def build_parser() -> ArgumentParser:
    """
    Builds an instance of command-line arguments parser
    :return: An Parser instance
    """
    parser = ArgumentParser()
    parser.add_argument("--config", help="File with configuration", default="")
    parser.add_argument("--skip-updates", default=False, help="Skip updates?", type=bool)

    return parser


def build_on_startup(config: configurator.BotConfig, client: Client):
    async def inner(dp: Dispatcher):
        utils.asyncio.schedule(jobs.messages_count_updater,
                               config.update_interval,
                               client,
                               dp,
                               config.served_chats)

    return inner


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

    storage = MemoryStorage()

    dispatcher = Dispatcher(bot, storage=storage)
    client = client_factory(config.userbot)

    # setup middlewares
    logging.info("Loading middlewares...")
    
    dispatcher.setup_middleware(
        SkipUpdateMiddleware(config.bot)
    )
    dispatcher.setup_middleware(
        TargetUserMiddleware(client)
    )
    dispatcher.setup_middleware(
        PyrogramClientMiddleware(client)
    )

    # setup filters
    logging.info("Loading filters...")
    dispatcher.filters_factory.bind(filters.IsAdmin)

    # setup handlers
    logging.info("Loading handlers...")
    handlers.setup(dispatcher)

    startup_func = build_on_startup(config.bot, client)

    executor.start_polling(
        dispatcher=dispatcher,
        skip_updates=args.skip_updates,
        on_startup=startup_func
    )


if __name__ == '__main__':
    main()
