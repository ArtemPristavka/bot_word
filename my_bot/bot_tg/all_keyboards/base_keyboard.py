from aiogram.utils.keyboard import KeyboardBuilder, ButtonType, ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def key_for_start_register() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="Регистриуемся"),
            KeyboardButton(text="Нет, спасибо") 
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard