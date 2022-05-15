import asyncio
import logging

from pyrogram import Client, errors
from aiogram import Dispatcher
from collections import Counter
from typing import List


async def messages_count_updater(client: Client, dp: Dispatcher, served_chats: List[int]):
    """
    Updates a count of messages in chat & saves it to Dispatcher's storage
    :param served_chats: A list with served chats
    :param client: A pyrogram client
    :param dp: A dispatcher
    :return: None
    """
    logging.info("Starting messages count updating...")
    
    for chat in served_chats:
        count = Counter()
        async for user in client.get_chat_members(chat):
            # iterate through chat members
            while True:
                # start loop
                # try to get messages count
                try:
                    msg_count = await client.search_messages_count(
                        chat_id=chat,
                        from_user=user.user.id
                    )
                except errors.FloodWait:
                    # if exception occur, sleep & continue
                    logging.info(f"Sleeping, because FloodWait raised")
                    await asyncio.sleep(10)
                    continue
                # if all is ok, save count to Counter & break
                count[user.user.id] = msg_count
                break

        data = await dp.storage.get_data(chat=chat)
        data["messages_count"] = count
        await dp.storage.set_data(chat=chat, data=data)
    # notice about finishing
    logging.info("Updating finished!")
