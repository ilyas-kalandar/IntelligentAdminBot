from typing import Callable

from aiogram import Dispatcher


def register_handler_with_base_filters(
        dispatcher: Dispatcher,
        handler: Callable, *args, **kwargs
):
    """
    Function, which registers a message handler with basic filters.
    """
    dispatcher.register_message_handler(
        handler,
        commands_prefix='!/',
        *args,
        **kwargs
    )
