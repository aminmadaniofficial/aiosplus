# نصب و راه‌اندازی (Installation)

کتابخانه **aiosplus** برای پایتون **3.10 و بالاتر** طراحی شده است.

---

## 📦 نصب از طریق PyPI

برای نصب آخرین نسخه پایدار کتابخانه از طریق مخزن رسمی پایتون (PyPI):

```bash
pip install aiosplus
```

---

## 🔌 نصب پکیج‌های اختیاری (Optional Dependencies)

کتابخانه `aiosplus` دارای ماژول‌های اختیاری برای پروژه‌های با مقیاس بزرگ است:

=== "پشتیبانی از Redis (FSM)"
    برای ذخیره‌سازی داده‌های ماشین وضعیت در دیتابیس Redis:
    ```bash
    pip install "aiosplus[redis]"
    ```

=== "پشتیبانی از FastAPI (Webhook)"
    برای استقرار وب‌هوک پرسرعت با فریم‌ورک FastAPI:
    ```bash
    pip install "aiosplus[fastapi]"
    ```

=== "نصب تمام بسته‌ها (All)"
    نصب تمامی وابستگی‌ها به‌صورت یکجا:
    ```bash
    pip install "aiosplus[all]"
    ```

---

## 🛠️ نصب نسخه توسعه (از گیت‌هاب)

اگر مایلید از آخرین تغییرات در شاخه `main` استفاده کنید:

```bash
pip install git+https://github.com/aminmadaniofficial/aiosplus.git
```
