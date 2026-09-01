"""نمونه کار با کیبوردهای اینلاین (Inline) و کیبوردهای معمولی (Reply).

Inline & Reply Keyboards example using aiosplus.
"""

import asyncio
import logging

from aiosplus import Bot, Dispatcher, F
from aiosplus.filters import Command
from aiosplus.types import CallbackQuery, Message
from aiosplus.utils import InlineKeyboardBuilder, ReplyKeyboardBuilder

logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("inline"))
async def cmd_inline(message: Message) -> None:
    """ارسال پیام به همراه اینلاین کیبورد چندردیفه."""
    builder = InlineKeyboardBuilder()
    builder.button(text="وبسایت سروش‌پلاس", url="https://splus.ir")
    builder.button(text="کلیک ۱", callback_data="btn:1")
    builder.button(text="کلیک ۲", callback_data="btn:2")
    builder.button(text="کلیک ۳", callback_data="btn:3")
    # چیدمان: ردیف اول ۱ دکمه (لینک)، ردیف دوم ۲ دکمه، ردیف سوم ۱ دکمه
    builder.adjust(1, 2, 1)

    await message.answer("یکی از گزینه‌های زیر را انتخاب کنید:", reply_markup=builder.as_markup())


@dp.callback_query(F.data.startswith("btn:"))
async def on_button_click(callback: CallbackQuery) -> None:
    """مدیریت رویداد کلیک دکمه‌های اینلاین."""
    btn_id = callback.data.split(":")[1] if callback.data else "0"
    await callback.answer(f"شما دکمه شماره {btn_id} را فشرده‌اید!", show_alert=True)

    if callback.message:
        await callback.message.edit_text(f"شما روی دکمه {btn_id} کلیک کردید.")


@dp.message(Command("reply"))
async def cmd_reply_keyboard(message: Message) -> None:
    """ارسال کیبورد معمولی (پایین صفحه) با امکان دریافت اطلاعات کاربر."""
    builder = ReplyKeyboardBuilder()
    builder.button(text="📞 ارسال شماره تماس", request_contact=True)
    builder.button(text="📍 ارسال موقعیت مکانی", request_location=True)
    builder.button(text="ℹ️ درباره ما")
    builder.button(text="❌ بستن کیبورد")
    builder.adjust(2, 2)

    await message.answer(
        "منوی اصلی ربات فعال شد:",
        reply_markup=builder.as_markup(
            resize_keyboard=True,
            input_field_placeholder="انتخاب از منو...",
        ),
    )


@dp.message(F.text == "ℹ️ درباره ما")
async def on_about(message: Message) -> None:
    await message.answer("این ربات با کتابخانه قدرتمند aiosplus نوشته شده است.")


async def main() -> None:
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
