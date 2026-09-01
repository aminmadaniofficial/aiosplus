"""اجرای ربات سروش‌پلاس در حالت وب‌هوک با استفاده از فریم‌ورک FastAPI.

FastAPI Webhook Server Example for aiosplus.
Requirements: pip install fastapi uvicorn
Run: uvicorn 05_webhook_fastapi:app --host 0.0.0.0 --port 8000
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aiosplus import Bot, Dispatcher
from aiosplus.filters import Command
from aiosplus.types import Message
from aiosplus.utils import SimpleWebhookHandler

logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN_HERE"
WEBHOOK_URL = "https://your-domain.com/webhook"

bot = Bot(token=TOKEN)
dp = Dispatcher()
webhook_handler = SimpleWebhookHandler(dispatcher=dp, bot=bot)


@dp.message(Command("start"))
async def on_start(message: Message) -> None:
    await message.answer("سلام! این ربات تحت وب‌هوک FastAPI در حال اجراست.")


@dp.message()
async def on_message(message: Message) -> None:
    if message.text:
        await message.answer(f"دریافت شد: {message.text}")


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    # راه‌اندازی وبهوک هنگام استارت سرور
    logging.info(f"Setting webhook to {WEBHOOK_URL}...")
    await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)
    yield
    # بستن سشن هنگام متوقف شدن سرور
    logging.info("Cleaning up webhook session...")
    await bot.close_session()


app = FastAPI(lifespan=lifespan)


@app.post("/webhook")
async def handle_webhook(request: Request) -> JSONResponse:
    """دریافت به‌روزرسانی‌های ورودی از سرورهای سروش‌پلاس."""
    try:
        raw_json: dict[str, Any] = await request.json()
        await webhook_handler.feed_raw_update(raw_json)
        return JSONResponse({"ok": True})
    except Exception as e:
        logging.error(f"Error handling webhook: {e}", exc_info=True)
        return JSONResponse({"ok": False, "error": str(e)}, status_code=500)
