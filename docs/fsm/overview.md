# ماشین وضعیت (Finite State Machine - FSM)

ماشین وضعیت (FSM) به ربات شما این امکان را می‌دهد که گفتگوهای مرحله‌به‌مرحله با کاربر داشته باشد (مانند فرم‌های ثبت‌نام، نظرسنجی‌ها، سبد خرید، فرآیند احراز هویت و ...).

---

## ۱. تعریف مراحل با `StatesGroup` و `State`

```python
from aiosplus import State, StatesGroup


class UserForm(StatesGroup):
    name = State()  # مرحله اول: دریافت نام
    age = State()  # مرحله دوم: دریافت سن
    city = State()  # مرحله سوم: دریافت شهر
```

---

## ۲. پیاده‌سازی گام‌به‌گام مراحل در هندلرها

```python
from aiosplus import Bot, Dispatcher, F, MemoryStorage
from aiosplus.filters import Command, StateFilter
from aiosplus.fsm.context import FSMContext
from aiosplus.types import Message

storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# گام ۱: شروع فرآیند با /register
@dp.message(Command("register"))
async def start_form(message: Message, state: FSMContext) -> None:
    await state.set_state(UserForm.name)
    await message.answer("لطفاً نام خود را وارد کنید:")


# گام ۲: دریافت نام و رفتن به مرحله سن
@dp.message(StateFilter(UserForm.name))
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await state.set_state(UserForm.age)
    await message.answer("سن خود را به صورت عدد وارد کنید:")


# گام ۳: دریافت سن و پایان فرم
@dp.message(StateFilter(UserForm.age))
async def process_age(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.isdigit():
        await message.answer("لطفاً فقط عدد وارد کنید:")
        return

    await state.update_data(age=int(message.text))
    data = await state.get_data()

    # نمایش خلاصه اطلاعات به کاربر
    await message.answer(f"✅ ثبت‌نام تکمیل شد!\nنام: {data['name']}\nسن: {data['age']}")

    # پاک‌سازی وضعیت کاربر
    await state.clear()
```

---

## ❌ لغو وضعیت در هر مرحله (`cancel`)

برای اینکه کاربر بتواند در هر مرحله عملیات را کنسل کند:

```python
@dp.message(Command("cancel"), StateFilter("*"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("هیچ عملیاتی در حال انجام نیست.")
        return

    await state.clear()
    await message.answer("عملیات با موفقیت لغو شد.")
```
