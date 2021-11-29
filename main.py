import asyncio
import logging

from dispatcher import dp
from aiogram.utils import executor
from handlers import register_handlers

# enable logging
logging.basicConfig(level=logging.INFO)

# create loop
loop = asyncio.get_event_loop()

# register handlers
register_handlers(dp)

# add asyncio tasks here...

if __name__ == '__main__':
    executor.start_polling(
        dispatcher=dp,
        loop=loop,
    )
