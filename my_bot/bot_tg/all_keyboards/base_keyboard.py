from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def key_for_start_register() -> ReplyKeyboardMarkup:
    "Клавиатура для регистрации"
    
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
    """
    Клавиатура для выбора действий пользователя

    Args:
        admin (bool, optional): Являеться ли этот пользователь администратором. 
            Defaults to False.

    Returns:
        ReplyKeyboardMarkup: 
    """
    
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


async def key_for_start_pay() -> ReplyKeyboardMarkup:
    "Клавиатура для оплаты"
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/pay")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    return keyboard