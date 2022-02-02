from aiogram import types, Dispatcher

import logging
import utils


async def process_captcha_answer(query: types.CallbackQuery):
    """
    Handles a passing of captcha
    :param query: A callback-query
    :return: None
    """

    tokens = query.data.split()
    verifiable_user_id = int(tokens[1])
    requester_id = query.from_user.id
    valid = tokens[2] == "True"

    logging.info(f"Processing captcha, {tokens} from {requester_id}")

    if verifiable_user_id != requester_id:
        await query.answer("This captcha is not for you :3")
        return

    await query.message.delete()

    if not valid:
        await query.bot.kick_chat_member(
            query.message.chat.id,
            verifiable_user_id
        )

        notice = await query.bot.send_message(
            query.message.chat.id,
            "User {} didn't pass a correct answer and kicked from chat.".format(
                utils.message.make_link(str(verifiable_user_id), verifiable_user_id)
            )
        )
        utils.asyncio.call_after(notice.delete, 20)
        return

    # so, if answer is valid, give all permissions to user
    await query.bot.restrict_chat_member(
        query.message.chat.id,
        verifiable_user_id,
        can_send_messages=True,
        can_send_media_messages=True,
        can_add_web_page_previews=True,
        can_send_other_messages=True
    )

    await query.answer("Welcome to chat!")


def setup_callback_query(dp: Dispatcher):
    """
    Setups a callback-query handlers
    :param dp: A Dispatcher instance
    :return: None
    """
    dp.register_callback_query_handler(process_captcha_answer,
                                       lambda q: q.data and q.data.startswith("captcha"),
                                       is_admin=False)
