from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from request_class import User
from all_keyboards.base_keyboard import (
    key_for_start_register, key_for_start_task
    )


async def command_start_handler(message: Message, state: FSMContext) -> None:
    """
    Обработчик команды старт

    Args:
        message (Message): Объект сообщения
        state (FSMContext): FormRegisterFSM
    """
    
    first_name = message.from_user.first_name # type: ignore
    last_name = message.from_user.last_name # type: ignore
    
    user = User(telegram_id=message.from_user.id) # type: ignore
    
    if user.have is False:
        keyboard = await key_for_start_register()
        await message.answer(
            f"Привет, " \
            f"{first_name if first_name else ''}" \
            f"{' ' + last_name if last_name else ''}" \
            f"\nЧто бы работать с тобой надо зарегистрироваться",
            reply_markup=keyboard
        )
    
    elif user.have is True:
        keyboard = await key_for_start_task(admin=user.admin) # type: ignore
        await message.answer(
            "Мы тебя помним",
            reply_markup=keyboard
        )
            

async def command_cancel_handler(message: Message, state: FSMContext) -> None:
    """
    Обработчик для команды отмены. Работает для всего

    Args:
        message (Message): Объект сообщения
        state (FSMContext): FormRegisterFSM
    """
    
    current_state = await state.get_state()
    if current_state is None:
        return 
    
    await state.clear()
    await message.answer(
        "Все-все, отменяю"
    )

    
async def event_from_base(dp: Dispatcher) -> None:
    """
    Регистрация базовых обработчиков событий для диспетчера

    Args:
        dp (Dispatcher):
    """
    
    dp.message.register(command_start_handler, CommandStart())
    dp.message.register(command_cancel_handler, Command("cancel"))