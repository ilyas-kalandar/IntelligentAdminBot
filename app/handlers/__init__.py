from aiogram import Dispatcher

from .adminitstrative import setup_administrative


def setup(dp: Dispatcher):
    setup_administrative(dp)
