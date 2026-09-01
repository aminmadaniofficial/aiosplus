# دیسپچر و روترها (Dispatcher & Routers)

کتابخانه `aiosplus` از معماری مدرن **بلوپرینت (Router)** مشابه aiogram 3 بهره می‌برد که ساخت ربات‌های بزرگ و چندبخشی را بسیار تمیز و سازمان‌یافته می‌کند.

---

## 🏗️ مفهوم Dispatcher و Router

- **`Dispatcher`**: روتر ریشه (Root Router) پروژه است که دریافت آپدیت‌ها و تغذیه آن‌ها به خط لوله فیلترها و میدل‌ویرها را مدیریت می‌کند.
- **`Router`**: زیرماژول‌ها و بخش‌های مختلف ربات (مثلاً بخش ادمین، بخش فروشگاه، بخش پشتیبانی) که درون Dispatcher یا سایر Routerها رجیستر می‌شوند (`include_router`).

---

## 🧩 ساختار ماژولار با روترها

فرض کنید می‌خواهید بخش ادمین را در یک فایل جداگانه (`handlers/admin.py`) بنویسید:

```python
# handlers/admin.py
from aiosplus import Router, F
from aiosplus.filters import Command
from aiosplus.types import Message

admin_router = Router(name="admin")

ADMIN_ID = 12345678

@admin_router.message(Command("panel"), F.from_user.id == ADMIN_ID)
async def admin_panel(message: Message) -> None:
    await message.answer("خوش آمدید ادمین گرامی!")
```

حالا در فایل اصلی پروژه (`main.py`) این روتر را متصل می‌کنیم:

```python
# main.py
import asyncio
from aiosplus import Bot, Dispatcher
from handlers.admin import admin_router

bot = Bot(token="YOUR_TOKEN")
dp = Dispatcher()

# الحاق روتر ادمین به دیسپچر اصلی
dp.include_router(admin_router)

async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 📡 انواع رویدادها در روتر

روترها از دکوراتورهای زیر برای رویدادهای مختلف پیام‌رسان پشتیبانی می‌کنند:

| دکوراتور | نوع رویداد دریافتی |
|---|---|
| `@router.message(*filters)` | دریافت پیام متنی، رسانه‌ای یا دستوری جدید |
| `@router.edited_message(*filters)` | ویرایش شدن یک پیام |
| `@router.callback_query(*filters)` | فشرده شدن دکمه‌های شیشه‌ای (Inline Keyboards) |
| `@router.update(*filters)` | دریافت هر نوع رویداد خام بدون فیلتر نوع |
