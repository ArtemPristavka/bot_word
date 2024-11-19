from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def key_for_choice_action() -> ReplyKeyboardMarkup:
    "Клавиаура для повтора задчи"
    
    buttons = [
        [
            KeyboardButton(text="/task"),
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    return keyboard