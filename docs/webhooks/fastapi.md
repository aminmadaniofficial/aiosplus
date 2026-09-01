# راه‌اندازی وب‌هوک با FastAPI (Webhooks)

برای پروژه‌های تولیدی با ترافیک بالا، اجرای ربات در حالت **Webhook** بازدهی و مقیاس‌پذیری بالاتری نسبت به Polling دارد.

---

## ⚡ پیاده‌سازی سرور وب‌هوک با FastAPI

```python
import logging
from contextlib import asynccontextmanager
from collections.abc import AsyncGenerator
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aiosplus import Bot, Dispatcher
from aiosplus.filters import CommandStart
from aiosplus.types import Message
from aiosplus.utils import SimpleWebhookHandler

logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN_HERE"
WEBHOOK_URL = "https://your-domain.com/webhook"

bot = Bot(token=TOKEN)
dp = Dispatcher()
webhook_handler = SimpleWebhookHandler(dispatcher=dp, bot=bot)


@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    await message.answer("سلام! این ربات بر روی سرور FastAPI در حال اجراست.")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # تنظیم وبهوک هنگام استارت سرور
    await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
    yield
    # بستن سشن هنگام خاموش شدن سرور
    await bot.close_session()


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def handle_webhook(request: Request) -> JSONResponse:
    """دریافت به‌روزرسانی‌های ورودی از سرور سروش‌پلاس."""
    try:
        raw_json: dict[str, Any] = await request.json()
        await webhook_handler.feed_raw_update(raw_json)
        return JSONResponse({"ok": True})
    except Exception as e:
        logging.error(f"Error handling webhook: {e}", exc_info=True)
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)
```

---

## 🚀 اجرای سرور با Uvicorn

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```
