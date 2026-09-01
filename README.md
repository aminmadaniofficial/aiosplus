# aiosplus 🚀

**aiosplus** is a modern, asynchronous, type-safe, and modular Python framework for the **Soroush Plus Bot API** ([سروش‌پلاس](https://soroushplus.com/p/documents/bot-platform)).

[![CI](https://github.com/aminmadaniofficial/aiosplus/actions/workflows/ci.yml/badge.svg)](https://github.com/aminmadaniofficial/aiosplus/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features | ویژگی‌ها

- ⚡ **Asynchronous First:** Built on top of Python `asyncio` and `httpx`.
- 🛡️ **Type Hinted & Validated:** 100% type annotations with **Pydantic v2** models.
- 🎯 **Aiogram 3 Style Architecture:** Modern Dispatcher, Routers, Middlewares, and Event Handlers.
- 🧠 **Finite State Machine (FSM):** Built-in state management and memory storage.
- ⌨️ **Fluent Keyboard Builders:** Chainable builders for Inline and Reply Keyboards.
- 📦 **100% Soroush Plus Bot API Coverage:** Full support for messages, files, media groups, stickers, webhooks, and long-polling.

---

## 📦 Installation | نصب

```bash
pip install aiosplus
```

---

## 🚀 Quickstart | شروع سریع

```python
import asyncio
from aiosplus import Bot, Dispatcher
from aiosplus.filters import Command
from aiosplus.types import Message

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher()


@dp.message(Command("start"))
async def start_handler(message: Message) -> None:
    await message.answer(
        f"سلام {message.from_user.first_name if message.from_user else 'دوست من'}! خوش آمدید."
    )


@dp.message()
async def echo_handler(message: Message) -> None:
    if message.text:
        await message.answer(f"شما گفتید: {message.text}")


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
