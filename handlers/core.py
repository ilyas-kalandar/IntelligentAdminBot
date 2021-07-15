from typing import Callable, Any

from aiogram import types, exceptions

from dispatcher import user_bot


def send_id(function: Callable[[types.Message, int, str], Any]):
    """
    Call to handler-function with ID of target
    If ID not exist (message is incorrect) sends error msg

    :param function:
    :return:
    """

    async def wrapper(message: types.Message):
        args = message.text.split()[1::]
        _id = None
        _full_name = None

        if message.reply_to_message:
            _id = message.reply_to_message.from_user.id
            _full_name = message.reply_to_message.from_user.full_name
        elif args:
            _username = args[0].removeprefix("@")
            try:
                user = await user_bot.get_user(message.chat.id,
                                               _username)
                _id = user.id
                _full_name = f"{user.first_name} {user.last_name if user.last_name else ''}"
            except ValueError:
                await message.answer(f"Failed, @{_username} not in group/blacklist.")
                return

        if not _id:
            await message.reply(
                "Please use provide a username or send message as reply to another message!"
            )
            return

        await function(message, _id, _full_name)

    return wrapper


def catch_exceptions(function: Callable):
    """
    Catch some Telegram-API exceptions

    :param Callable function: A function
    :return: Wrapped function
    :rtype: Callable
    """

    async def wrapper(message: types.Message):
        try:
            await function(message)
        except exceptions.UserIsAnAdministratorOfTheChat:
            await message.answer("Oh, shit, user is administrator.")
        except exceptions.CantRestrictChatOwner:
            await message.answer("Chat owner cooler than me :/")
        except exceptions.ChatAdminRequired:
            await message.answer("I am not admin.")

    return wrapper
