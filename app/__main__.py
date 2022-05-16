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
from middlewares import (
    TargetUserMiddleware,
    SkipUpdateMiddleware,
    PyrogramClientMiddleware,
)


def client_factory(config: configurator.UserBotConfig) -> Client:
    """
    Returns an initialized client
    :param config: A UserBot configuration
    :return: Pyrogram Client
    """
    client = Client(
        api_hash=config.api_hash,
        api_id=config.api_id,
        name="pyrogram",
    )

    client.start()

    return client


def parser_factory() -> ArgumentParser:
    """
    Builds an instance of command-line arguments parser
    :return: An Parser instance
    """
    parser = ArgumentParser()
    parser.add_argument("--config", help="File with configuration", default="")

    return parser


def on_startup_factory(config: configurator.BotConfig, client: Client):
    """
    Creates a async-function for making some jobs before starting dispath
    :param config: A Bot-Configuration
    :param client: A pyrogram client
    """

    async def inner(dp: Dispatcher):
        utils.asyncio.schedule(
            jobs.messages_count_updater,
            config.update_interval,
            client,
            dp,
            config.served_chats,
        )

    return inner


def load_config(config_path: str) -> configurator.Config:
    """
    Loads a configuration
    :param config_path: A string with path
    :return: A Config-object
    """

    if config_path.endswith(".ini"):
        return configurator.load_from_ini(config_path)
    elif config_path.endswith(".env"):
        return configurator.load_from_dotenv(config_path)
    else:
        return configurator.load_from_environ()


def configure_logging(config: configurator.BotConfig):
    """
    Configures logging
    :param config: A Bot-Configuration
    :return: None
    """

    logging_level = logging.INFO

    if config.bot.debug:
        logging_level = logging.DEBUG

    logging.basicConfig(level=logging_level)


def main():
    """Heart of project"""

    # setup command line arguments parser
    parser = parser_factory()
    # parse
    args = parser.parse_args()
    # load configuration
    config = load_config(args.config)
    # Initialize bot
    bot = Bot(config.bot.token, parse_mode="html")
    logging.info(f"Intelligent Bot, version {BOT_VERSION}")
    # Initialize Dispatcher
    logging.info("Initializing Dispatcher")
    storage = MemoryStorage()
    dispatcher = Dispatcher(bot, storage=storage)
    logging.info("Initializing pyrogram_client")
    client = client_factory(config.userbot)

    # setup middlewares
    logging.info("Loading middlewares...")

    dispatcher.setup_middleware(SkipUpdateMiddleware(config.bot))
    dispatcher.setup_middleware(TargetUserMiddleware(client))
    dispatcher.setup_middleware(PyrogramClientMiddleware(client))

    # setup filters
    logging.info("Loading filters...")
    dispatcher.filters_factory.bind(filters.IsAdmin)

    # setup handlers
    logging.info("Loading handlers...")
    handlers.setup(dispatcher)

    startup_func = on_startup_factory(config.bot, client)

    executor.start_polling(
        dispatcher=dispatcher,
        skip_updates=config.bot.skip_updates,
        on_startup=startup_func,
    )


if __name__ == "__main__":
    main()
