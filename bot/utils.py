import asyncio
from asyncio import sleep
from configparser import ConfigParser
from typing import Awaitable, Callable

from easydict import EasyDict


def mention_user(full_name: str, user_id: int) -> str:
    """
    Returns a mention-link to user
    :param full_name: A fullname of user
    :param user_id: An ID of user in telegram
    :return: Link
    :rtype: str
    """
    return f"<a href='tg://user?id={user_id}'>{full_name}</a>"


def call_after(func: Callable[[...], Awaitable], delay: int, *args, **kwargs):
    """
    Calls async function after ```delay``` seconds
    :param func: An async function
    :param delay: Delay time (in seconds)
    :param args: An arguments for func
    :param kwargs: Keyword-Arguments for func
    """

    async def inner_func():
        await sleep(delay)
        await func(*args, **kwargs)

    asyncio.create_task(inner_func())


def get_config(filename: str) -> EasyDict:
    """
    :param filename: A name of .ini file
    :return: An EasyDict object with configuration!!!
    """

    parser = ConfigParser()
    parser.read(filename)
    config = EasyDict()

    if not parser.sections():
        raise ValueError("Invalid file was been given!")

    for section in parser.sections():
        config[section] = EasyDict()

        for key, value in parser.items(section):
            config[section][key] = value

    return config
