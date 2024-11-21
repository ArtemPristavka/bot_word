from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from final_state import FormTaskFSM
from request_class import User
from config import MAX_FREE_CALL
from all_keyboards.task_keyboard import key_for_choice_action
from all_keyboards.base_keyboard import key_for_start_register, key_for_start_pay
from typing import List
import collections
import re


async def handeler_start_task(message: Message, state: FSMContext) -> None:
    """
    Старторвый обработчик для решения задач от пользователей

    Args:
        message (Message): 
        state (FSMContext): FormTaskFSM

    Returns:
        _type_: _description_
    """
    user = User(telegram_id=message.from_user.id) # type: ignore
    if not user.have:
        keyboard = await key_for_start_register()
        await message.answer(
            "Для начала надо зарегистрироваться",
            reply_markup=keyboard
        )
        
        return # Что б дальше не проходило
    
    if not user.admin:
        if not user.subscription:
            if user.count_call > MAX_FREE_CALL: # type: ignore
                keyboard = await key_for_start_pay()
                await message.answer(
                    "Бесплатные попытки закончились!\n" \
                    "Надо оформить подписку",
                    reply_markup=keyboard
                )
            
                return # Что бы дальше не проходило
    
    await state.set_state(FormTaskFSM.start_task)
    await message.answer(
        "Введи предложение:"
    )
    

async def handler_count_word_from_sentence(message: Message, state: FSMContext) -> None:
    """
    Подсчет частоты слов в предложении и отправка результатов пользователю

    Args:
        message (Message): 
        state (FSMContext): FormTaskFSM
    """
    
    user = User(telegram_id=message.from_user.id) # type: ignore
    user.send_call()
    
    # Очистка текста от различных знаков 
    clear_text: str = re.sub("[^\sA-Za-zА-Яа-я]", " ", message.text) # type: ignore
    clear_text: str = re.sub("\s+", " ", clear_text)
    split_text: List[str] = clear_text.lower().split() # type: ignore
    
    counting_words = collections.Counter(split_text)
    # TODO добавить убывающию сортировку, что бы от большего повторения слов к меньшему
    futury_msg = [
        f"{i_word} ---> {i_count}"
        for i_word, i_count in counting_words.items()
    ]
    msg_answer = "\n".join(futury_msg)
    
    keyboard = await key_for_choice_action()
    await state.clear()
    await message.answer(
        "Частота слов в твоем предложении:\n" \
        f"{msg_answer}",
        reply_markup=keyboard
    )
    
    
async def event_from_task(dp: Dispatcher) -> None:
    """
    Регистрация обработчиков событий задачи для диспетчера

    Args:
        dp (Dispatcher):
    """
    dp.message.register(handeler_start_task, Command("task"))
    dp.message.register(handler_count_word_from_sentence, FormTaskFSM.start_task)

