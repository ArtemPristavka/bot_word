from aiogram import Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from final_state import FormAdminFSM
from request_class import User
from all_requests import get_statistic
from all_keyboards.admin_keyboard import (
    key_action_admin, 
    key_choice_month_admin, 
    key_choice_day_admin, 
    key_show_statistic
)


async def start_admin_panel(message: Message, state: FSMContext) -> None:
    """
    Старт панели администратора

    Args:
        message (Message): 
        state (FSMContext): 
    """
    user = User(telegram_id=message.from_user.id) # type: ignore
    if user.admin:
        keyboard = await key_action_admin()
        await state.set_state(FormAdminFSM.choice_action)
        await message.answer(
            "Админ панель:",
            reply_markup=keyboard
        )
    
    else: # Защита от посторонних 
        await message.answer(
            text="У вас нет доступа"
        )

async def choice_action(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Выбор действия администратором

    Args:
        callback (CallbackQuery):
        state (FSMContext): 
    """

    # Для выбора даты 
    if callback.data == "date": 
        await state.set_state(FormAdminFSM.choice_month)
        keyboard = await key_choice_month_admin()
        await callback.message.edit_text( # type: ignore
            text="Выбери месяц:",
            reply_markup=keyboard
        )
    
    # Для показа статистики
    elif callback.data == "show":
        data = await state.get_data()
        
        try:
            count_call = get_statistic(data['month'], data['day']) 
        except KeyError:
            count_call = "Нету"
            
        keyboard = await key_show_statistic()
        await callback.message.edit_text( # type: ignore
            text=f"Кол-во совершенных запросов пользователями: {count_call}",
            reply_markup=keyboard
        )
    
    # Для возврата со слайда статистики
    elif callback.data == "back":
        data = await state.get_data()
        
        keyboard = await key_action_admin()
        await callback.message.edit_text( # type: ignore
            text="Админь панель\n" \
                f"Выбранная дата: месяц: {data['month']} | день: {data['day']} ",
            reply_markup=keyboard
        )


async def choice_date_day(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Сохранение выбранного месяца и предложение выбрать день

    Args:
        callback (CallbackQuery): 
        state (FSMContext): 
    """
    
    await state.update_data(month=callback.data)
    
    keyboard = await key_choice_day_admin()
    await state.set_state(FormAdminFSM.choice_day)
    await callback.message.edit_text( # type: ignore
        text="Выбери день:",
        reply_markup=keyboard
    )
    

async def save_data_day(callback: CallbackQuery, state: FSMContext) -> None:
    """
    Сохранение выбранного дня и переходи на главый слайд администратора

    Args:
        callback (CallbackQuery): 
        state (FSMContext): 
    """
    
    await state.update_data(day=callback.data)
    await state.set_state(FormAdminFSM.choice_action)
    
    data = await state.get_data()
    keyboard = await key_action_admin()
    await callback.message.edit_text( # type: ignore
        text="Админь панель\n" \
            f"Выбранная дата: месяц: {data['month']} | день: {data['day']} ",
        reply_markup=keyboard
    )
    
    
async def event_for_admin(dp: Dispatcher) -> None:
    """
    Регистрация событий администратора для диспетчера

    Args:
        dp (Dispatcher): _description_
    """
    dp.message.register(start_admin_panel, Command("admin"))
    dp.callback_query.register(choice_action, FormAdminFSM.choice_action)
    dp.callback_query.register(choice_date_day, FormAdminFSM.choice_month)
    dp.callback_query.register(save_data_day, FormAdminFSM.choice_day)