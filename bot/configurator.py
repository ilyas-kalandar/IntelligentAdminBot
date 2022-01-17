from configparser import ConfigParser
from dataclasses import dataclass


@dataclass
class Configuration:
    """
    Just Config representation
    """
    bot_token: str
    captcha_expiration_time: int
    user_bot_api_hash: str
    user_bot_api_id: int


def load_config(filename: str) -> Configuration:
    """
    Loads a configuration
    :param filename: A name of .ini file
    :return: A Configuration object
    """

    parser = ConfigParser()
    parser.read(filename)

    bot_token = parser.get(
        "bot", "token"
    )

    captcha_expiration_time = int(parser.get(
        "captcha", "expiration_time"
    ))

    user_bot_api_hash = parser.get(
        "userbot", "api_hash"
    )

    user_bot_api_id = int(
        parser.get("userbot", "api_id")
    )

    return Configuration(
        bot_token,
        captcha_expiration_time,
        user_bot_api_hash,
        user_bot_api_id
    )
