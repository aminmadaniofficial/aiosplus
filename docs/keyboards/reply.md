# کیبوردهای معمولی و متنی (Reply Keyboards)

کیبوردهای معمولی در پایین صفحه چت کاربر قرار می‌گیرند و با کلیک روی آنها، متن دکمه به عنوان یک پیام عادی به ربات فرستاده می‌شود.

---

## 🏗️ استفاده از `ReplyKeyboardBuilder`

```python
from aiosplus import Bot, Dispatcher, F
from aiosplus.filters import Command
from aiosplus.types import Message, ReplyKeyboardRemove
from aiosplus.utils import ReplyKeyboardBuilder

@dp.message(Command("start"))
async def start_with_menu(message: Message) -> None:
    builder = ReplyKeyboardBuilder()

    builder.button(text="🛍️ محصولات")
    builder.button(text="💳 کیف پول")
    builder.button(text="⚙️ تنظیمات")
    builder.button(text="❌ بستن کیبورد")

    # چیدمان: سطر اول ۲ دکمه، سطر دوم ۲ دکمه
    builder.adjust(2, 2)

    await message.answer(
        "منوی اصلی فعال شد:",
        reply_markup=builder.as_markup(
            resize_keyboard=True, # کوچک کردن دکمه‌ها متناسب با صفحه
            input_field_placeholder="انتخاب از منو...",
        ),
    )
```

---

## 🗑️ بستن و حذف کیبورد (`ReplyKeyboardRemove`)

هنگامی که می‌خواهید کیبورد پایین صفحه برداشته شود:

```python
@dp.message(F.text == "❌ بستن کیبورد")
async def close_menu(message: Message) -> None:
    await message.answer(
        "کیبورد بسته شد.",
        reply_markup=ReplyKeyboardRemove(),
    )
```
