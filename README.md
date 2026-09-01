# aiosplus 🚀

**aiosplus** is a modern, high-performance, asynchronous, type-safe, and modular Python framework for the **Soroush Plus Bot API** ([مستندات پلتفرم بات سروش‌پلاس](https://soroushplus.com/p/documents/bot-platform)).

[![CI](https://github.com/aminmadaniofficial/aiosplus/actions/workflows/ci.yml/badge.svg)](https://github.com/aminmadaniofficial/aiosplus/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Pydantic v2](https://img.shields.io/badge/pydantic-v2-E92063.svg)](https://docs.pydantic.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Features | ویژگی‌های کلیدی

- ⚡ **Asynchronous First:** Built from the ground up on Python's `asyncio` and `httpx` for maximum concurrency and throughput.
- 🛡️ **Pydantic V2 Powered:** Complete, strictly-typed data models with automatic JSON validation and serialization for all API entities.
- 🎯 **Aiogram 3 Style Architecture:** Modular `Dispatcher`, `Router` blueprints, `EventObserver`, and hierarchical middleware pipelines.
- 🪄 **Expressive Magic Filters (`F`):** Clean and readable query filtering like `F.text == "hello"`, `F.from_user.id == 123`, `F.data.startswith("action_")`.
- 🧠 **Finite State Machine (FSM):** Built-in state management with `StatesGroup`, `State`, `FSMContext`, and `MemoryStorage`.
- ⌨️ **Fluent Keyboard Builders:** Chainable `InlineKeyboardBuilder` and `ReplyKeyboardBuilder` for dynamic button layouts.
- 📦 **100% Soroush Plus Bot API Coverage:** Full support for messages, photos, audio, documents, videos, voice notes, video notes, media albums, contacts, locations, stickers, bot commands, webhooks, and long polling.
- 🔤 **Rich Formatting Utilities:** Helpers for HTML and MarkdownV2 text formatting and character escaping.

---

## 📦 Installation | نصب

Install using pip:

```bash
pip install aiosplus
```

Or install with FastAPI webhook support:

```bash
pip install "aiosplus[fastapi]"
```

---

## 🚀 Quickstart | شروع سریع

Create your first bot in fewer than 20 lines of code:

```python
import asyncio
from aiosplus import Bot, Dispatcher
from aiosplus.filters import Command
from aiosplus.types import Message

# Initialize Bot and Dispatcher
bot = Bot(token="YOUR_BOT_TOKEN_HERE")
dp = Dispatcher()


# Handle /start command
@dp.message(Command("start"))
async def start_handler(message: Message) -> None:
    user_name = message.from_user.first_name if message.from_user else "کاربر"
    await message.answer(f"سلام {user_name}! خوش آمدید به ربات سروش‌پلاس.")


# Echo text messages
@dp.message()
async def echo_handler(message: Message) -> None:
    if message.text:
        await message.answer(f"شما گفتید: {message.text}")


async def main() -> None:
    print("Bot is running...")
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🧩 Architecture Overview | ساختار معماری

```
aiosplus/
├── bot/               # Core Bot client handling API requests & file transfers
├── client/            # Async HTTP session & URL construction (HTTPX)
├── dispatcher/        # Dispatcher, Routers, Event Observers, & Pipelines
├── enums.py           # ParseMode, ChatType, MessageEntityType, ChatAction, etc.
├── exceptions.py      # Comprehensive API & network exception hierarchy
├── filters/           # Command, Text, MagicFilter (F), ChatType, State filters
├── fsm/               # Finite State Machine (StatesGroup, FSMContext, MemoryStorage)
├── middlewares/       # Outer & Inner middleware abstract bases
├── types/             # Pydantic v2 data models for all Soroush Plus objects
└── utils/             # Keyboard builders, text formatters, & webhook helpers
```

---

## 📚 Guides & Examples | راهنما و مثال‌ها

Explore ready-to-run examples in the [`examples/`](examples/) directory:

1. **[Echo Bot](examples/01_echo_bot.py):** Basic message handling and command dispatching.
2. **[Keyboards Bot](examples/02_keyboards_bot.py):** Multi-row inline keyboards, callback query alerts, and reply menus.
3. **[FSM Survey Bot](examples/03_fsm_survey_bot.py):** Multi-step form data collection using `StatesGroup` and `FSMContext`.
4. **[Media & Files Bot](examples/04_media_and_files_bot.py):** Uploading photos, sending albums (`send_media_group`), and downloading user files.
5. **[FastAPI Webhook](examples/05_webhook_fastapi.py):** High-throughput production webhook server with FastAPI.

---

### ⌨️ Dynamic Keyboards Example

```python
from aiosplus.utils import InlineKeyboardBuilder

builder = InlineKeyboardBuilder()
builder.button(text="وبسایت", url="https://splus.ir")
builder.button(text="تایید", callback_data="confirm")
builder.button(text="انصراف", callback_data="cancel")
builder.adjust(1, 2)  # Row 1: 1 button, Row 2: 2 buttons

await message.answer("گزینه مورد نظر را انتخاب کنید:", reply_markup=builder.as_markup())
```

---

### 🧠 Finite State Machine (FSM) Example

```python
from aiosplus import State, StatesGroup
from aiosplus.fsm.context import FSMContext
from aiosplus.filters import StateFilter


class Form(StatesGroup):
    name = State()
    age = State()


@dp.message(Command("register"))
async def start_register(message: Message, state: FSMContext) -> None:
    await state.set_state(Form.name)
    await message.answer("لطفاً نام خود را وارد کنید:")


@dp.message(StateFilter(Form.name))
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(Form.age)
    await message.answer("سن خود را وارد کنید:")
```

---

## 📡 API Methods Supported | متدهای پشتیبانی‌شده

| Method | Soroush Plus Endpoint | Return Type |
|---|---|---|
| `get_me` | `/getMe` | `User` |
| `send_message` | `/sendMessage` | `Message` |
| `forward_message` | `/forwardMessage` | `Message` |
| `copy_message` | `/copyMessage` | `MessageId` |
| `send_photo` | `/sendPhoto` | `Message` |
| `send_audio` | `/sendAudio` | `Message` |
| `send_document` | `/sendDocument` | `Message` |
| `send_video` | `/sendVideo` | `Message` |
| `send_animation` | `/sendAnimation` | `Message` |
| `send_voice` | `/sendVoice` | `Message` |
| `send_video_note` | `/sendVideoNote` | `Message` |
| `send_media_group` | `/sendMediaGroup` | `list[Message]` |
| `send_location` | `/sendLocation` | `Message` |
| `send_contact` | `/sendContact` | `Message` |
| `send_sticker` | `/sendSticker` | `Message` |
| `send_chat_action` | `/sendChatAction` | `bool` |
| `get_file` | `/getFile` | `File` |
| `download_file` | `/file/bot<token>/<path>` | `Path / BinaryIO` |
| `answer_callback_query`| `/answerCallbackQuery` | `bool` |
| `set_my_commands` | `/setMyCommands` | `bool` |
| `get_my_commands` | `/getMyCommands` | `list[BotCommand]` |
| `delete_my_commands` | `/deleteMyCommands` | `bool` |
| `edit_message_text` | `/editMessageText` | `Message / bool` |
| `edit_message_caption` | `/editMessageCaption` | `Message / bool` |
| `edit_message_media` | `/editMessageMedia` | `Message / bool` |
| `edit_message_reply_markup` | `/editMessageReplyMarkup` | `Message / bool` |
| `delete_message` | `/deleteMessage` | `bool` |
| `get_updates` | `/getUpdates` | `list[Update]` |
| `set_webhook` | `/setWebhook` | `bool` |
| `delete_webhook` | `/deleteWebhook` | `bool` |
| `get_webhook_info` | `/getWebhookInfo` | `WebhookInfo` |

---

## 🧪 Testing & Quality Assurance

Run the test suite with coverage:

```bash
pytest
```

Run type checking and code formatting:

```bash
mypy aiosplus tests
ruff check .
ruff format .
```

---

## 📄 License

This project is licensed under the terms of the [MIT License](LICENSE).
