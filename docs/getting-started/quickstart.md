# شروع سریع (Quickstart)

در این راهنما، اولین ربات پیام‌رسان سروش‌پلاس خود را با استفاده از کتابخانه `aiosplus` می‌سازیم.

---

## ۱. دریافت توکن ربات از سروش‌پلاس

1. وارد پیام‌رسان سروش‌پلاس شوید.
2. به بات رسمی ساخت و مدیریت ربات‌ها مراجعه کنید.
3. یک ربات جدید ایجاد کرده و **توکن (Token)** اختصاصی آن را کپی کنید.

---

## ۲. نوشتن کد ربات اکو

یک فایل به نام `bot.py` ایجاد کرده و کدهای زیر را درون آن قرار دهید:

```python
import asyncio
import logging

from aiosplus import Bot, Dispatcher, F
from aiosplus.filters import CommandStart
from aiosplus.types import Message

# فعال‌سازی لاگ‌ها برای مشاهده روند اجرای درخواست‌ها
logging.basicConfig(level=logging.INFO)

# مقداردهی اولیه کلاینت بات و دیسپچر
TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start_handler(message: Message) -> None:
    """هندلر دستور /start."""
    user_name = message.from_user.first_name if message.from_user else "کاربر"
    await message.answer(f"سلام {user_name}! خوش آمدید به ربات سروش‌پلاس.")


@dp.message()
async def echo_handler(message: Message) -> None:
    """اکو کردن تمام پیام‌های متنی دریافتی."""
    if message.text:
        await message.answer(f"🤖 شما گفتید: {message.text}")


async def main() -> None:
    print("در حال راه‌اندازی ربات در حالت Long Polling...")
    # متد start_polling پیام‌های در انتظار قبلی را پاک کرده و به صورت خودکار پیام‌ها را دریافت می‌کند
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## ۳. اجرای ربات

اسکریپت را با پایتون اجرا کنید:

```bash
python bot.py
```

اکنون وارد سروش‌پلاس شده و به ربات خود پیام `/start` یا یک متن دلخواه بفرستید! 🎉
