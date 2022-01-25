from aiogram import types


def make_link(full_name: str, user_id: int):
    """
    Returns a link to user
    :param full_name:
    :param user: A telegram user
    :param
    :return: Link of user
    """
    return f"<a href='tg://user?id={user_id}'>{full_name}</a>"


def get_arguments(message: types.Message):
    """

    :param message:
    :return:
    """

    return message.text.split()[1::]
