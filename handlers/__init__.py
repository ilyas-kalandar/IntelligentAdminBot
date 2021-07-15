from aiogram import Dispatcher

from .admin_actions import register_admin_actions
from .events import register_event_handlers
from .user_actions import register_user_handlers


def register_handlers(dp: Dispatcher):
    """
    Register handlers
    :param dp: A aiogram's dispatcher
    :return:
    """

    register_admin_actions(dp)
    register_event_handlers(dp)
