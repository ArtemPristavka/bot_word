from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import date
from all_requests import get_min_date


async def key_action_admin() -> InlineKeyboardMarkup:
    "Клавиатура для действий администратора"
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Выбрать дату",
                    callback_data="date"
                ),
                InlineKeyboardButton(
                    text="Посмотреть",
                    callback_data="show"
                )
            ]
        ]
    )
    
    return keyboard


async def key_choice_month_admin() -> InlineKeyboardMarkup:
    "Клавиатура для выбора месяца администратором"
    
    min_data = get_min_date()
    now = date.today()
    
    buttons = list()
    for i_month in range(min_data["month"], now.month + 1):
        buttons.append(
            InlineKeyboardButton(
                text=f"{i_month}",
                callback_data=f"{i_month}"
            )
        )
        
    return InlineKeyboardMarkup(inline_keyboard=[buttons]) 

async def key_choice_day_admin() -> InlineKeyboardMarkup:
    "Клавиатура для выбора дня администратором"
    
    min_date = get_min_date()
    now = date.today() 
    # TODO сделать что бы выводилось нужное число в зависимости от кол-во дней в месяце
    
    buttons = list()
    for i_day in range(min_date["day"], now.day + 1):
        buttons.append(
            InlineKeyboardButton(
                text=f"{i_day}",
                callback_data=f"{i_day}"
            )
        )
        
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


async def key_show_statistic() -> InlineKeyboardMarkup:
    "Клавиатура для слайда показа статистики"
    
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="<< Назад",
                    callback_data="back"
                )
            ]
        ]
    )
