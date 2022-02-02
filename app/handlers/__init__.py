from aiogram import Dispatcher

from .adminitstrative import setup_administrative
from .captcha import setup_captcha
from .default import setup_default
from .callback_query import setup_callback_query
from .service_messages import setup_service_message_handler


def setup(dp: Dispatcher):
    """
    Setups a default-handlers
    :param dp: Dispatcher instance
    :return: None
    """
    setup_administrative(dp)
    setup_captcha(dp)
    setup_default(dp)
    setup_callback_query(dp)
    setup_service_message_handler(dp)
