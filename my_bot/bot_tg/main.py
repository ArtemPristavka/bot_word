import asyncio

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message


TOKEN = ""

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    first_name = message.from_user.first_name # type: ignore
    last_name = message.from_user.last_name # type: ignore
    await message.answer(
        f"Hello, " \
        f"{first_name if first_name else ''}" \
        f"{' ' + last_name if last_name else ''}"
    )


@dp.message()
async def echo_handler(message: Message) -> None:
    # msm = message.text
    await message.answer(message.text) # type: ignore


async def main() -> None:
    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
