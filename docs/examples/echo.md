# ربات اکو (Echo Bot)

ساده‌ترین ربات برای بررسی صحت اتصال و دریافت پیام‌ها:

```python
import asyncio
import logging

from aiosplus import Bot, Dispatcher
from aiosplus.filters import CommandStart, CommandHelp
from aiosplus.types import Message

logging.basicConfig(level=logging.INFO)

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()


@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    await message.answer("سلام! به ربات اکو خوش آمدید.")


@dp.message(CommandHelp())
async def on_help(message: Message) -> None:
    await message.answer("هر متنی بفرستید، عیناً برای شما بازگردانده می‌شود.")


@dp.message()
async def on_echo(message: Message) -> None:
    if message.text:
        await message.answer(f"پیام شما: {message.text}")


async def main() -> None:
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
```
