import asyncio
import logging
from dispatcher import dp
from handlers import register_handlers

# enable logging
logging.basicConfig(level=logging.INFO)

# create loop
loop = asyncio.get_event_loop()

# register handlers
register_handlers(dp)

# create asyncio tasks
loop.create_task(dp.start_polling())

if __name__ == '__main__':
    loop.run_forever()