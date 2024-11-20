from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from request_class import User
from config import PROVIDER_TOKE


async def order_buy_subscription(message: Message, bot: Bot) -> None:
    """
    Обработчик старта оплаты.
    Проверяет пользователя на админку и подписку.

    Args:
        message (Message): 
        bot (Bot): 
    """
    
    user = User(telegram_id=message.from_user.id) # type: ignore
    if user.admin:
        await message.answer(
            text="Зачем тебе подписка?\nТы же админ"
        )
        
    elif not user.subscription:
        await bot.send_invoice(
            chat_id=message.chat.id,
            title="Подписка на бота",
            description="Оплата подписки на бота",
            payload="Subscription",
            currency="RUB",
            prices=[
                LabeledPrice(label="Подписка", amount=500_00)
            ],
            provider_token=PROVIDER_TOKE, # В config 
            start_parameter="MovieBbot",
            disable_notification=False,
            protect_content=True
        )
    
    elif user.subscription:
        await message.answer(
            text="У тебя есть подписка.\nВсе хорошо!"
        )


async def pre_checkout_query(pre_checkout_query: PreCheckoutQuery, bot: Bot) -> None:
    """
    Обработчик подтверждения что бот готов предоставить продукт

    Args:
        pre_checkout_query (PreCheckoutQuery): 
        bot (Bot): 
    """
    
    await bot.answer_pre_checkout_query(
        pre_checkout_query_id=pre_checkout_query.id,
        ok=True
    )
    

async def successful_payment(message: Message) -> None:
    """
    Обработчк успешной оплаты.
    Оформление подписки для пользователя

    Args:
        message (Message): 
    """
    
    user = User(telegram_id=message.from_user.id) # type: ignore
    if user.send_subscription():
        await message.answer(
            text="Подписка оформлена"
        )
    
    else:
        await message.answer(
            text="Что то пошло не так"
        )
 
 
async def event_from_pay(dp: Dispatcher) -> None:
    """
    Регистрация обработчик собый оплаты для диспетчера

    Args:
        dp (Dispatcher): 
    """
    
    dp.message.register(order_buy_subscription, Command("pay"))
    dp.pre_checkout_query.register(pre_checkout_query)
    dp.message.register(successful_payment, F.successful_payment)