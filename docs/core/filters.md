# فیلترها و Magic Filter (`F`)

فیلترها تعیین می‌کنند کدام هندلر باید یک پیام یا رویداد خاص را پردازش کند.

---

## 🪄 فیلتر جادویی (Magic Filter `F`)

کتابخانه `aiosplus` آبجکت قدرتمند `F` را در اختیار شما می‌گذارد که امکان شرط‌گذاری بسیار سریع و خوانا را فراهم می‌کند:

### مثال‌های فیلتر متن:
```python
from aiosplus import F

# برابری متن دقیق
@dp.message(F.text == "سلام")

# شروع با یک عبارت خاص
@dp.message(F.text.startswith("سفارش:"))

# پایان با عبارت خاص
@dp.message(F.text.endswith(".pdf"))

# شامل بودن یک زیررشته
@dp.message(F.text.contains("تخفیف"))

# عضویت در لیست کلمات
@dp.message(F.text.in_(["بله", "خیر", "شاید"]))

# فیلتر با رجکس (Regex)
@dp.message(F.text.regexp(r"^/order_\d+$"))
```

### مثال‌های فیلتر کاربر و چت:
```python
# فقط برای یک کاربر خاص (مثلاً ادمین)
@dp.message(F.from_user.id == 12345678)

# فقط برای چت‌های خصوصی
@dp.message(F.chat.type == "private")

# پیام‌های حاوی تصویر
@dp.message(F.photo)

# پیام‌های حاوی فایل (Document)
@dp.message(F.document)
```

### ترکیب شرط‌ها با عملگرهای بیتی:
```python
# ترکیب AND با &
@dp.message((F.from_user.id == 12345) & F.text.startswith("admin:"))

# ترکیب OR با |
@dp.message((F.text == "شروع") | (F.text == "راهنما"))

# نقیض (NOT) با ~
@dp.message(~F.text.contains("اسپم"))
```

---

## ⌨️ فیلترهای اختصاصی دستورات (`Command`)

```python
from aiosplus.filters import Command, CommandStart, CommandHelp, CommandObject

# فیلتر دستور /start
@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    ...

# فیلتر دستور /start با دیپ‌لینک (Deep-linking)
# مثلاً کاربر با لینک https://splus.ir/mybot?start=ref_123 وارد شده است
@dp.message(CommandStart(deep_link=r"ref_\d+"))
async def on_ref_start(message: Message, command: CommandObject) -> None:
    referrer_id = command.args
    await message.answer(f"شما با شناسه معرف {referrer_id} وارد شدید.")

# فیلتر دستور /help
@dp.message(CommandHelp())

# فیلتر چند دستور همزمان
@dp.message(Command(["settings", "config"]))
```
