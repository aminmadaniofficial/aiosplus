"""نمونه ارسال و دریافت انواع رسانه‌ها (عکس، فایل، ویس، ویدیو و آلبوم).

Media and File Handling Bot using aiosplus.
"""

import asyncio
import logging
from pathlib import Path

from aiosplus import Bot, Dispatcher, F
from aiosplus.filters import Command
from aiosplus.types import InputFile, InputMediaPhoto, Message

logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("send_photo"))
async def cmd_send_photo(message: Message) -> None:
    """ارسال یک تصویر از سیستم یا از طریق URL."""
    # روش ۱: ارسال فایل از روی دیسک
    photo_path = Path("sample.jpg")
    if photo_path.exists():
        await message.answer_photo(
            photo=InputFile(photo_path),
            caption="این تصویر از حافظه محلی ارسال شده است.",
        )
    else:
        # روش ۲: ارسال از طریق آدرس اینترنتی مستقیم
        await message.answer_photo(
            photo="https://splus.ir/assets/images/logo.png",
            caption="تصویر لوگوی سروش‌پلاس از وب.",
        )


@dp.message(Command("send_album"))
async def cmd_send_album(message: Message) -> None:
    """ارسال چند رسانه به صورت آلبوم (Media Group)."""
    media_group = [
        InputMediaPhoto(media="https://splus.ir/assets/images/logo.png", caption="عکس اول"),
        InputMediaPhoto(media="https://splus.ir/assets/images/logo.png", caption="عکس دوم"),
    ]
    await bot.send_media_group(chat_id=message.chat.id, media=media_group)


@dp.message(F.photo)
async def on_user_photo(message: Message) -> None:
    """دریافت عکس ارسالی توسط کاربر و دانلود آن."""
    if message.photo:
        # بالاترین کیفیت عکس (آخرین عنصر در لیست)
        highest_res_photo = message.photo[-1]
        file_info = await bot.get_file(highest_res_photo.file_id)

        dest_dir = Path("downloads")
        dest_dir.mkdir(exist_ok=True)
        saved_file = dest_dir / f"{highest_res_photo.file_unique_id}.jpg"

        await bot.download_file(file_info, destination=saved_file)
        await message.answer(
            f"تصویر شما با موفقیت با سایز {highest_res_photo.file_size} بایت ذخیره شد."
        )


@dp.message(F.document)
async def on_user_document(message: Message) -> None:
    """دریافت فایل متفرقه و نمایش مشخصات آن."""
    if message.document:
        doc = message.document
        await message.answer(
            f"📄 فایل دریافتی: {doc.file_name}\n"
            f"📦 حجم: {doc.file_size} بایت\n"
            f"🏷 پسوند/نوع: {doc.mime_type}"
        )


async def main() -> None:
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
