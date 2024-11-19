from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def key_for_start_register() -> ReplyKeyboardMarkup:
    # TODO дописать docstring
    buttons = [
        [
            KeyboardButton(text="/register"),
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )

    return keyboard

async def key_for_start_task(admin: bool = False) -> ReplyKeyboardMarkup:
    # TODO дописать docstring
    buttons = [
        [
            KeyboardButton(text="/task")
        ]
    ]
    if admin:
        buttons[0].append(
            KeyboardButton(text="/admin")
        )
        
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    return keyboard