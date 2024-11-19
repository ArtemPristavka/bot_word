import asyncio

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers.handlers_base import even_from_base
from handlers.handlers_register import even_from_register


TOKEN = "6105356535:AAHdG6IlfOZpY2k5WnUXaMHJlvjE4WDyoog"


async def on_startup_for_dp(dp: Dispatcher) -> None:
    """
    Регистрация обработчиков

    Args:
        dp (Dispatcher): диспетчер
    """
    
    await even_from_base(dp) # Базовый должен быть первым что бы работала отмена
    await even_from_register(dp)


async def main() -> None:
    "Функция запуска"
    
    dp = Dispatcher()
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    await on_startup_for_dp(dp)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
