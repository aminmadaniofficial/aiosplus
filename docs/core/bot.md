# کلاینت ربات (Bot Client)

کلاس `Bot` قلب تپنده ارتباط شما با سرورهای پیام‌رسان سروش‌پلاس است. این کلاس تمامی متدهای استاندارد پلتفرم بات را با متدهای ناهمگام (Async) پایتون پیاده‌سازی می‌کند.

---

## 🌟 مقداردهی اولیه

```python
from aiosplus import Bot
from aiosplus.enums import ParseMode

bot = Bot(
    token="YOUR_BOT_TOKEN",
    default_parse_mode=ParseMode.HTML,  # تنظیم پیش‌فرض فرمت پیام‌ها (HTML یا MarkdownV2)
)
```

---

## 🛠️ متدهای پرکاربرد

### ۱. ارسال پیام متنی (`send_message`)

```python
msg = await bot.send_message(
    chat_id=12345678,
    text="سلام! این یک پیام <b>مهم</b> است.",
    parse_mode=ParseMode.HTML,
)
```

### ۲. ارسال تصویر (`send_photo`)

ارسال تصویر از طریق URL، فایل سیستم یا بایت‌ها:

```python
from pathlib import Path
from aiosplus.types import InputFile

# روش اول: با آدرس اینترنتی
await bot.send_photo(
    chat_id=12345678,
    photo="https://splus.ir/assets/images/logo.png",
    caption="لوگوی رسمی سروش‌پلاس",
)

# روش دوم: از روی دیسک سیستم
await bot.send_photo(
    chat_id=12345678,
    photo=InputFile(Path("banner.jpg")),
    caption="بنر تبلیغاتی",
)
```

### ۳. دریافت مشخصات فایل و دانلود آن (`download_file`)

```python
from pathlib import Path

# دریافت متادیتای فایل از سرور
file_info = await bot.get_file(file_id="FILE_ID_HERE")

# دانلود و ذخیره مستقیم روی دیسک
dest_path = Path("downloads/photo.jpg")
await bot.download_file(file_info, destination=dest_path)
```

### ۴. ویرایش و حذف پیام (`edit_message_text`, `delete_message`)

```python
# ویرایش متن
await bot.edit_message_text(
    chat_id=12345678,
    message_id=105,
    text="متن جدید و ویرایش‌شده",
)

# حذف پیام
await bot.delete_message(chat_id=12345678, message_id=105)
```

---

## 💡 متدهای میانبر روی اشیاء (Convenience Methods)

هنگامی که یک `Message` در هندلر دریافت می‌کنید، نیازی به صدا زدن مستقیم `bot.send_message` ندارید و می‌توانید از متدهای میانبر استفاده نمایید:

```python
@dp.message()
async def on_message(message: Message) -> None:
    # ارسال پیام جدید در همین چت
    await message.answer("پاسخ شما داده شد.")

    # ریپلای مستقیم روی پیام کاربر
    await message.reply("این پیام ریپلای شد.")

    # ارسال تصویر در همین چت
    await message.answer_photo("https://splus.ir/logo.png", caption="عکس تستی")

    # حذف همین پیام
    await message.delete()
```
