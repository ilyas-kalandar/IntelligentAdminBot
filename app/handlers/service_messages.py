from aiogram import Dispatcher, types


async def service_messages_handler(message: types.Message):
    """
    Deletes unwanted service messages
    :param message:
    :return:
    """
    await message.delete()


def setup_service_message_handler(dp: Dispatcher):
    """
    Setups a service messages handler
    :param dp: A dispatcher
    :return: None
    """
    dp.register_message_handler(service_messages_handler, content_types=["left_chat_members"])
