from aiogram import types
from typing import List


def make_link(full_name: str, user_id: int) -> str:
    """
    Returns a link to user
    :param full_name: Full name of user
    :param user_id: A user's id
    :return: Link of user
    """

    return f"<a href='tg://user?id={user_id}'>{full_name}</a>"


def get_arguments(message: types.Message) -> List[str]:
    """
    Returns arguments of command in message
    :param message: A message
    :return: An arguments provided in message
    """

    return message.text.split()[1::]
