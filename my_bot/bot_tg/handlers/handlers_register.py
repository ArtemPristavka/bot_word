from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from final_state import FormRegisterFSM
from request_class import User
from all_requests import register_user
from all_keyboards.base_keyboard import key_for_start_task
import requests


async def input_first_passowrd(message: Message, state: FSMContext) -> None:
    """
    Обработчик для предложения ввести пароль

    Args:
        message (Message): Объект сообщения
        state (FSMContext): FormRegisterFSM
    """

    user = User(telegram_id=message.from_user.id) # type: ignore
    if user.have:
        await message.answer(
            "Мы тебя помним!\n" \
            "Тебе не надо регистрироваться"
        )
        
        return # Что бы дальше не проходило
    
    await state.set_state(FormRegisterFSM.start_register)
    await message.answer(
        "Придумай и введи пароль.\n" \
        "Требования к паролю:\n" \
        "Он должен состоять из различным символов, букв и цифр, пароль " \
        "не может быть меньше 8 символов.\n" \
        "Придумай пароль:"
    )
    

async def input_second_password(message: Message, state: FSMContext) -> None:
    """
    Обработчик проверки первого введенного пароля по требованиям.
    И переход дальше

    Args:
        message (Message): Объект сообщения
        state (FSMContext): FormRegisterFSM
    """
    
    async def check_password(password: str) -> bool:
        """
        Проверяем первый пароль на наличие букв, цифр
        и наименьшей длинны

        Args:
            password (str): пароль

        Returns:
            bool: True при пройденной проверки
        """
        # TODO переписать на регулярку
        if len(password) < 8:
            return False
        
        number = False
        symbol = False
        
        for i_sym in password:
             
            if i_sym.isdigit():
                number = True
                continue
            
            if i_sym.isalpha():
                symbol = True
            
        if number is True and symbol is True:
            return True
        
        return False
    
    
    result_check = await check_password(message.text) # type: ignore
    if result_check:
        await state.update_data(password_1=message.text)
        await state.set_state(FormRegisterFSM.password)
        await message.answer(
            "Хорошо, введи пароль еще раз"
        )
    
    else:
        await message.answer(
            "Не соблюдаешь требования к паролю.\n" \
            "Придумай пароль:"
        )
    

async def check_passwords(message: Message, state: FSMContext) -> None:
    """
    Обработчки сравнения двух введенных паролей

    Args:
        message (Message): Объект сообщения
        state (FSMContext): FormRegisterFSM
    """
    
    password_1 = await state.get_value("password_1")
    password_2 = message.text
    
    if password_1 != password_2:
        await state.update_data(password_1=None)
        await state.set_state(FormRegisterFSM.start_register)
        await message.answer(
            "Пароли не совпадают. Начнем с начала.\n" \
            "Придумай пароль:"
        )
    
    else:
        result = register_user(
            message.from_user.username, # type: ignore
            password_1, # type: ignore
            message.from_user.id # type: ignore
        )
        
        if result:
            keyboard = await key_for_start_task()
            await state.clear()
            await message.answer(
                "Все отлично, не забудь его!\n" \
                "Используй ник как логин.",
                reply_markup=keyboard
            )
        
        # else:
        #     await state.set_state(FormRegisterFSM.start_register)
        #     await message.answer(
        #         "Что то пошло не так"
        #     )
        
    
    
async def event_from_register(dp: Dispatcher) -> None:
    """
    Регистрация обработчиков событий для диспетчера

    Args:
        dp (Dispatcher): Dispatcher
    """
    
    dp.message.register(input_first_passowrd, Command("register"))
    dp.message.register(input_second_password, FormRegisterFSM.start_register)
    dp.message.register(check_passwords, FormRegisterFSM.password)