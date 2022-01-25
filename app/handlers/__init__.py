from aiogram import Dispatcher

from .adminitstrative import setup_administrative
from .captcha import setup_captcha


def setup(dp: Dispatcher):
    setup_administrative(dp)
    setup_captcha(dp)
