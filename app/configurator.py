from dataclasses import dataclass
from configparser import ConfigParser

from typing import List

import envparse


@dataclass
class BotConfig:
    token: str
    debug: bool
    served_chats: List[int]
    update_interval: int


@dataclass
class UserBotConfig:
    api_hash: str
    api_id: int


@dataclass
class Config:
    bot: BotConfig
    userbot: UserBotConfig


def load_from_ini(filename: str) -> Config:
    """
    Loads the app-configuration
    :return: A configuration-object
    :rtype: Config
    """
    parser = ConfigParser()
    parser.read(filename)

    # Load app-settings

    token = parser.get("bot", "token")
    debug = parser.getboolean("bot", "debug")
    served_chats = list(map(int, parser.get("bot", "served_chats").split(',')))
    update_interval = parser.getint("bot", "update_interval")
    bot_config = BotConfig(token, debug, served_chats, update_interval)

    # load user-app settings

    api_hash = parser.get("userbot", "api_hash")

    api_id = parser.getint("userbot", "api_id")

    user_bot_config = UserBotConfig(api_hash, api_id)

    return Config(
        bot_config,
        user_bot_config
    )


def load_from_environ() -> Config:
    """
    Loads config from environ using envparse lib
    :return: Configuration
    """
    # Load app-settings

    bot_token = envparse.env.str("INTELLIGENT_BOT_TOKEN")
    debug = envparse.env.bool("INTELLIGENT_BOT_DEBUG")
    served_chats = list(map(int, envparse.env.str("INTELLIGENT_BOT_SERVED_CHATS")))
    update_interval = envparse.env("INTELLIGENT_BOT_UPDATE_INTERVAL")
    bot_config = BotConfig(bot_token, debug, served_chats, update_interval)

    # load user-bot settings

    api_hash = envparse.env.str("INTELLIGENT_USERBOT_API_HASH")
    api_id = envparse.env.int("INTELLIGENT_USERBOT_API_ID")

    user_bot_config = UserBotConfig(api_hash=api_hash, api_id=api_id)

    return Config(
        bot_config,
        user_bot_config
    )


def load_from_dotenv(filename: str) -> Config:
    """
    Loads config to environ & returns a configuration-object
    :param filename: A string with filename
    """
    envparse.env.read_envfile(filename, overrides=True)
    return load_from_environ()
