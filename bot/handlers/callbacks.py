from aiogram import Dispatcher
from aiogram.types import CallbackQuery


async def check_captcha(query: CallbackQuery):
    verifiable_user_id = int(query.from_user.id)
    user_id_from_request = int(query.data.split()[1])

    if verifiable_user_id != user_id_from_request:
        await query.answer("This captcha is not for you :3")
        return

    await query.answer("Ok, welcome to our chat")

    # give all permissions
    
    await query.bot.restrict_chat_member(
        query.message.chat.id,
        verifiable_user_id,
        can_send_messages=True,
        can_send_media_messages=True,
        can_add_web_page_previews=True,
        can_send_other_messages=True
    )
    await query.message.delete()


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        check_captcha,
        lambda x: x.data.startswith('captcha')
    )
