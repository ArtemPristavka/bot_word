from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from final_state import FormRegisterFSM

import requests


async def input_first_passowrd(message: Message, state: FSMContext) -> None:
    """
    Обработчик для преложения ввести пароль

    Args:
        message (Message): Объект сообщения
        state (FSMContext): FormRegisterFSM
    """
    
    await state.set_state(FormRegisterFSM.password_1)
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
        await state.set_state(FormRegisterFSM.password_2)
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
        await state.set_state(FormRegisterFSM.password_1)
        await message.answer(
            "Пароли не совпадают. Начнем с начала.\n" \
            "Придумай пароль:"
        )
    
    else:
        response = requests.post(
            url="http://127.0.0.1:8000/telegram/users/",
            data={
                "username": message.from_user.username, # type: ignore
                "password": password_1,
                "telegram_id": message.from_user.id # type: ignore
            }
        )
        if response.status_code == 201:
            await state.clear()
            await message.answer(
                "Все отлично, не забудь его!"
            )
        
        else:
            await state.set_state(FormRegisterFSM.password_1)
            await message.answer(
                "Что то пошло не так"
            )
        
    
    
async def even_from_register(dp: Dispatcher) -> None:
    """
    Регистрация обработчиков событий для диспетчера

    Args:
        dp (Dispatcher): Dispatcher
    """
    
    dp.message.register(input_first_passowrd, FormRegisterFSM.start_register)
    dp.message.register(input_second_password, FormRegisterFSM.password_1)
    dp.message.register(check_passwords, FormRegisterFSM.password_2)