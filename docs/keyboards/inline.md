# دکمه‌های شیشه‌ای و اینلاین (Inline Keyboards)

دکمه‌های اینلاین در زیر متن پیام قرار گرفته و می‌توانند کاربر را به یک لینک منتقل کنند یا با کلیک روی آنها، یک داده پنهان (`callback_data`) برای ربات ارسال شود.

---

## 🏗️ استفاده از `InlineKeyboardBuilder`

سازنده زنجیره‌ای `InlineKeyboardBuilder` ساخت کیبوردهای چندردیفه را بسیار ساده می‌کند:

```python
from aiosplus import Bot, Dispatcher, F
from aiosplus.filters import Command
from aiosplus.types import CallbackQuery, Message
from aiosplus.utils import InlineKeyboardBuilder

@dp.message(Command("menu"))
async def show_menu(message: Message) -> None:
    builder = InlineKeyboardBuilder()

    # افزودن دکمه‌های لینک و کال‌بک
    builder.button(text="🌐 وبسایت سروش‌پلاس", url="https://splus.ir")
    builder.button(text="🛒 خرید اشتراک", callback_data="buy:pro")
    builder.button(text="ℹ️ راهنما", callback_data="info")
    builder.button(text="📞 پشتیبانی", callback_data="support")

    # چیدمان سطری: سطر اول ۱ دکمه، سطر دوم ۲ دکمه، سطر سوم ۱ دکمه
    builder.adjust(1, 2, 1)

    await message.answer(
        "منوی خدمات ربات:",
        reply_markup=builder.as_markup(),
    )
```

---

## ⚡ مدیریت کلیک دکمه‌ها (`callback_query`)

برای دریافت و پردازش کلیک روی دکمه‌های اینلاین:

```python
# فیلتر کلیک دکمه‌هایی که دیتای آن‌ها با buy: شروع می‌شود
@dp.callback_query(F.data.startswith("buy:"))
async def on_buy_click(callback: CallbackQuery) -> None:
    plan = callback.data.split(":")[1]

    # ۱. نمایش پیام پاپ‌آپ (Alert) به کاربر
    await callback.answer(f"شما پلن {plan} را انتخاب کردید!", show_alert=True)

    # ۲. ویرایش پیام قبلی
    if callback.message:
        await callback.message.edit_text(f"سفارش شما برای پلن {plan} ثبت شد.")
```
