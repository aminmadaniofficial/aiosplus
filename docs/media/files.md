# ارسال و دانلود فایل‌ها (Files & Media)

کتابخانه `aiosplus` کار با انواع فایل‌های چندرسانه‌ای (عکس، ویدیو، صدا، سند، ویس و استیکر) را بسیار روان کرده است.

---

## 📤 ارسال فایل با `InputFile`

برای ارسال فایل از حافظه محلی سیستم، از کلاس `InputFile` استفاده می‌شود:

```python
from pathlib import Path
from aiosplus.types import InputFile

# ارسال فایل متفرقه (PDF / ZIP / DOCX)
await bot.send_document(
    chat_id=12345678,
    document=InputFile(Path("catalogue.pdf")),
    caption="کاتالوگ محصولات جدید",
)

# ارسال ویدیو
await bot.send_video(
    chat_id=12345678,
    video=InputFile(Path("video.mp4")),
    caption="ویدیوی آموزشی",
)
```

---

## 📥 دانلود فایل‌های ارسالی کاربر

هنگامی که کاربر برای ربات عکس یا فایلی ارسال می‌کند، ابتدا `file_id` آن را دریافت کرده و سپس فایل را دانلود می‌کنید:

```python
from pathlib import Path
from aiosplus import F
from aiosplus.types import Message


# هندلر دریافت عکس
@dp.message(F.photo)
async def on_user_photo(message: Message) -> None:
    if message.photo:
        # دریافت بالاترین کیفیت (آخرین سایز در آرایه)
        highest_photo = message.photo[-1]

        # دریافت اطلاعات مسیر فایل از سرور
        file_info = await bot.get_file(highest_photo.file_id)

        # مسیر مقصد برای ذخیره‌سازی
        save_path = Path("downloads") / f"{highest_photo.file_unique_id}.jpg"
        save_path.parent.mkdir(exist_ok=True)

        # دانلود مستقیم روی دیسک
        await bot.download_file(file_info, destination=save_path)
        await message.answer("تصویر شما با موفقیت دانلود و ذخیره شد.")
```
