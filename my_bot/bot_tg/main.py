import asyncio
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand
from handlers.handlers_base import even_from_base
from handlers.handlers_register import even_from_register
from handlers.handlers_task import even_from_task
from handlers.handlers_admin import even_for_admin


TOKEN = "6105356535:AAHdG6IlfOZpY2k5WnUXaMHJlvjE4WDyoog"


async def on_startup_for_dp(dp: Dispatcher) -> None:
    """
    Регистрация обработчиков

    Args:
        dp (Dispatcher): диспетчер
    """
    
    await even_from_base(dp) # Базовый должен быть первым что бы работала отмена
    await even_from_register(dp)
    await even_from_task(dp)
    await even_for_admin(dp)
    

async def on_startup_for_bot(bot: Bot) -> None:
    commands = [
        BotCommand(command="/start", description="Start work with bot"),
        BotCommand(command="/task", description="Task for bot"),
        BotCommand(command="/register", description="Registe by bot"),
        BotCommand(command="/admin", description="Show admin panel"),
        BotCommand(command="/cancel", description="Cancel this action")
    ]
    await bot.set_my_commands(commands=commands)


async def main() -> None:
    "Функция запуска"
    
    dp = Dispatcher()
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    await on_startup_for_dp(dp)
    await on_startup_for_bot(bot)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
