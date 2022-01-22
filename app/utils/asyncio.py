from typing import Callable, Coroutine

import asyncio


def call_after(func: Callable[[...], Coroutine], delay: int, *args, **kwargs):
    """
    Calls async function after ```delay``` seconds
    :param func: An async function
    :param delay: Delay time (in seconds)
    :param args: An arguments for func
    :param kwargs: Keyword-Arguments for func
    """

    async def inner_func():
        await asyncio.sleep(delay)
        await func(*args, **kwargs)

    asyncio.create_task(inner_func())
