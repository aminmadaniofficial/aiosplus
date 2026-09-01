# فضاهای ذخیره‌سازی FSM (Storages)

کتابخانه `aiosplus` از دو نوع فضای ذخیره‌سازی برای نگهداری داده‌های ماشین وضعیت پشتیبانی می‌کند:

---

## ۱. `MemoryStorage` (برای ربات‌های تک‌سرور و توسعه)

تمام داده‌ها در RAM سرور ذخیره می‌شوند. بسیار سریع است اما با ری‌استارت شدن ربات، داده‌های موقت پاک می‌شوند:

```python
from aiosplus import Dispatcher, MemoryStorage

storage = MemoryStorage()
dp = Dispatcher(storage=storage)
```

---

## ۲. `RedisStorage` (برای ربات‌های پرترافیک و توزیع‌شده)

داده‌ها در سرور Redis ذخیره می‌شوند. داده‌ها در صورت ری‌استارت شدن بات محفوظ مانده و می‌توان چند نمونه (Instance) از ربات را به‌طور همزمان اجرا کرد:

```python
from aiosplus import Dispatcher, RedisStorage

# ایجاد استوریج ریدیس با زمان انقضای دلخواه (TTL)
storage = RedisStorage.from_url(
    "redis://localhost:6379/0",
    key_prefix="splus_fsm",
    state_ttl=3600,  # انقضای وضعیت پس از ۱ ساعت عدم فعالیت
    data_ttl=3600,
)

dp = Dispatcher(storage=storage)
```
