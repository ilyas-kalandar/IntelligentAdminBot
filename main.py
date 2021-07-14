import asyncio

from dispatcher import dp, bot
from handlers import register_handlers

# create loop
loop = asyncio.get_event_loop()

# register handlers
register_handlers(dp)


# register filters

loop.create_task(dp.start_polling())

if __name__ == '__main__':
    loop.run_forever()
