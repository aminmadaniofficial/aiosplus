<div class="hero-container">
    <div class="hero-title">aiosplus 🚀</div>
    <div class="hero-subtitle">
        فریم‌ورک مدرن، ناهمگام (Async)، ماژولار و تایپ‌استریکت پایتون برای ساخت ربات‌های پیام‌رسان سروش‌پلاس
    </div>
    <div>
        <a href="getting-started/quickstart/" class="md-button md-button--primary">شروع سریع ⚡</a>
        <a href="https://github.com/aminmadaniofficial/aiosplus" class="md-button">مشاهده در گیت‌هاب ⭐️</a>
    </div>
</div>

<div class="feature-grid">
    <div class="feature-card">
        <div class="feature-icon">⚡</div>
        <div class="feature-title">سرعت و همزمانی بالا</div>
        <div class="feature-desc">طراحی شده بر پایه asyncio و httpx برای هندل کردن هزاران پیام همزمان بدون افت سرعت.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🛡️</div>
        <div class="feature-title">تایپ‌استریکت با Pydantic v2</div>
        <div class="feature-desc">اعتبارسنجی دقیق داده‌ها، تایپ‌هینت کامل و تبدیل خودکار پاسخ‌های API به آبجکت‌های پایتونی.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🎯</div>
        <div class="feature-title">معماری ماژولار Aiogram 3</div>
        <div class="feature-desc">استفاده از Dispatcher، Router، EventObserver و پایپ‌لاین قدرتمند Middleware.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🪄</div>
        <div class="feature-title">فیلترهای جادویی (Magic Filter F)</div>
        <div class="feature-desc">فیلترنویسی تمیز و خوانا بدون نیاز به توابع پیچیده: <code>F.text == 'سلام'</code>.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">🧠</div>
        <div class="feature-title">ماشین وضعیت (FSM)</div>
        <div class="feature-desc">مدیریت فرم‌ها و نظرسنجی‌های چندمرحله‌ای با پشتیبانی از MemoryStorage و RedisStorage.</div>
    </div>
    <div class="feature-card">
        <div class="feature-icon">⌨️</div>
        <div class="feature-title">سازنده زنجیره‌ای کیبورد</div>
        <div class="feature-desc">ساخت داینامیک دکمه‌های شیشه‌ای (Inline) و کیبوردهای معمولی با متد هوشمند <code>adjust</code>.</div>
    </div>
</div>

---

## ⚡ نمونه کد در یک نگاه

```python
import asyncio
from aiosplus import Bot, Dispatcher, F
from aiosplus.filters import Command, CommandStart
from aiosplus.types import Message

# ایجاد کلاینت ربات و دیسپچر
bot = Bot(token="YOUR_BOT_TOKEN_HERE")
dp = Dispatcher()

# پاسخ به دستور /start
@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    await message.answer(f"سلام {message.from_user.first_name}! خوش آمدید.")

# فیلتر پیام‌های خاص با Magic Filter F
@dp.message(F.text == "سلام")
async def on_hello(message: Message) -> None:
    await message.reply("سلام و درود! چطور می‌تونم کمکتون کنم؟")

async def main() -> None:
    print("ربات با موفقیت فعال شد...")
    await dp.start_polling(bot, drop_pending_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🧭 مسیر یادگیری

- **[نصب و راه‌اندازی](getting-started/installation.md):** راهنمای نصب با pip و پکیج‌های اختیاری.
- **[اولین ربات](getting-started/quickstart.md):** ساخت ربات اکو قدم به قدم.
- **[کلاینت ربات (Bot)](core/bot.md):** آشنایی با متدهای ارسال متن، عکس، ویدیو، آلبوم و مدیریت ربات.
- **[فیلترها و Magic Filter](core/filters.md):** فیلترنویسی پیشرفته برای پیام‌ها، دکمه‌ها و فرم‌ها.
- **[ماشین وضعیت (FSM)](fsm/overview.md):** ساخت فرم‌های چندمرحله‌ای با ذخیره‌سازی داده.
