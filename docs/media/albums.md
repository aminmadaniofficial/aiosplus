# آلبوم‌های چندرسانه‌ای (Media Groups)

با متد `send_media_group` می‌توانید چندین عکس یا ویدیو را در قالب یک آلبوم واحد ارسال نمایید.

---

## 📸 ارسال آلبوم عکس

```python
from aiosplus.types import InputMediaPhoto, InputMediaVideo

media_album = [
    InputMediaPhoto(
        media="https://splus.ir/assets/images/photo1.jpg",
        caption="تصویر اول از آلبوم",
    ),
    InputMediaPhoto(
        media="https://splus.ir/assets/images/photo2.jpg",
    ),
    InputMediaPhoto(
        media="https://splus.ir/assets/images/photo3.jpg",
    ),
]

messages = await bot.send_media_group(
    chat_id=12345678,
    media=media_album,
)
```
