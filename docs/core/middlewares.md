# میان‌افزارها (Middlewares)

میان‌افزارها (Middlewares) به شما اجازه می‌دهند قبل و بعد از اجرای هندلرها، عملیاتی مانند لاگ‌برداری، کنترل دسترسی (Authentication)، محدودسازی نرخ درخواست (Rate Limiting) یا تزریق دیتابیس را انجام دهید.

---

## 🛠️ ساخت میان‌افزار سفارشی

برای ساخت میان‌افزار، کافی است از کلاس `BaseMiddleware` ارث‌بری کرده و متد `__call__` را پیاده‌سازی کنید:

```python
from typing import Any, Awaitable, Callable
from aiosplus import BaseMiddleware

class SimpleAuthMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        # کدهای قبل از اجرای هندلر (Pre-processing)
        user_id = getattr(event, "from_user", None) and event.from_user.id
        print(f"دریافت پیام از کاربر: {user_id}")

        # می‌توان متغیرهای کمکی را به آرگومان‌های هندلر تزریق کرد
        data["is_authenticated"] = True

        # فراخوانی هندلر اصلی
        result = await handler(event, data)

        # کدهای بعد از اجرای هندلر (Post-processing)
        print("پایان پردازش پیام.")
        return result
```

---

## 🔌 ثبت میان‌افزار در روتر یا دیسپچر

```python
dp = Dispatcher()

# ثبت میان‌افزار برای تمام پیام‌های ورودی
dp.message.middleware(SimpleAuthMiddleware())

# یا استفاده از میدل‌ویر آماده لاگینگ کتابخانه
from aiosplus import LoggingMiddleware
dp.message.middleware(LoggingMiddleware())
```
