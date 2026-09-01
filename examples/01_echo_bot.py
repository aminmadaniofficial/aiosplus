"""ساده‌ترین ربات اکو با کتابخانه aiosplus.

Simple Echo Bot using aiosplus.
"""

import asyncio
import logging

from aiosplus import Bot, Dispatcher
from aiosplus.filters import Command
from aiosplus.types import Message

# تنظیمات لاگینگ
logging.basicConfig(level=logging.INFO)

# ساخت نمونه ربات و دیسپچر
TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    """پاسخ به دستور /start."""
    user_name = message.from_user.first_name if message.from_user else "کاربر گرامی"
    await message.answer(f"سلام {user_name}! خوش آمدید به ربات سروش‌پلاس.")


@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    """پاسخ به دستور /help."""
    await message.answer("هر پیامی برای من ارسال کنید، من همان را برای شما تکرار می‌کنم!")


@dp.message()
async def echo_handler(message: Message) -> None:
    """اکو کردن تمام پیام‌های متنی ورودی."""
    if message.text:
        await message.answer(f"پیام شما: {message.text}")


async def main() -> None:
    print("Starting bot in polling mode...")
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
