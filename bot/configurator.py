from dataclasses import dataclass
from configparser import ConfigParser


@dataclass
class BotConfig:
    TOKEN: str


@dataclass
class UserBotConfig:
    API_HASH: str
    API_ID: int


@dataclass
class Config:
    BOT: BotConfig
    USERBOT: UserBotConfig


def load_config(filename: str) -> Config:
    """
    Loads the bot-configuration
    :return: A configuration-object
    :rtype: Config
    """
    parser = ConfigParser()
    parser.read(filename)

    # Load bot-settings

    token = parser.get("bot", "token")

    bot_config = BotConfig(token)

    # load user-bot settings

    api_hash = parser.get("userbot", "api_hash")

    api_id = parser.getint("userbot", "api_id")

    user_bot_config = UserBotConfig(api_hash, api_id)

    return Config(
        bot_config,
        user_bot_config
    )
