from aiogram import Dispatcher
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from final_state import FormTaskFSM
from request_class import User
from all_keyboards.task_keyboard import key_for_choice_action
from all_keyboards.base_keyboard import key_for_start_register, key_for_start_pay
import collections


async def handeler_start_task(message: Message, state: FSMContext) -> None:
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
            if user.count_call > 5: # type: ignore
                keyboard = await key_for_start_pay()
                await message.answer(
                    "Бесплатные попытки закончились!\n" \
                    "Надо оформить подписку",
                    reply_markup=keyboard
                )
            # TODO кол-во бесплатных запросов можно вынеси в конфиг
            # TODO сделать перенаправление на оплату подписки
            
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
    
    # TODO добавить регулярку на знаки, что бы очистить предложение от них
    split_text = message.text.split() # type: ignore
    counting_words = collections.Counter(split_text)
    futury_msg = [
        f"{i_word} --> {i_count}"
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

