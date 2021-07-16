from aiogram import Dispatcher
from aiogram.types import CallbackQuery


async def check_captcha(query: CallbackQuery):
    _id1 = int(query.from_user.id)
    _id2 = int(query.data.split()[1])

    if _id1 == _id2:
        await query.answer("Ok, welcome to our chat")
        await query.bot.restrict_chat_member(
            # give all permissions
            query.message.chat.id,
            _id1,
            can_send_messages=True,
            can_send_media_messages=True,
            can_add_web_page_previews=True,
            can_send_other_messages=True
        )
        return await query.message.delete()

    await query.answer("This captcha <b>not</b> for you :3")


def register_callback_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(
        check_captcha,
        lambda x: x.data.startswith('captcha')
    )
