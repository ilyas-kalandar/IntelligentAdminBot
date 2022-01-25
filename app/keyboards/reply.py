from aiogram import types
import random


def gen_captcha_keyboard(for_user: int, valid_answer: int) -> types.InlineKeyboardMarkup:
    """
    Generates a keyboard with answers of captcha
    :param for_user: An ID of user which will be checked
    :param valid_answer: An valid answer of captcha
    :return:
    """

    keyboard = types.InlineKeyboardMarkup()
    keyboard.row_width = 4

    answers = [
        valid_answer,
        valid_answer + 1,
        valid_answer - 1,
        valid_answer + 2,
    ]

    random.shuffle(answers)

    for answer in answers:
        valid = "valid" if answer == valid_answer else "invalid"
        data = f"captcha {for_user} {valid}"
        key = types.InlineKeyboardButton(
            text=str(answer),
            callback_data=data
        )

        keyboard.insert(key)

    return keyboard
