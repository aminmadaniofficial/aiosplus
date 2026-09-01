# ربات فرم و نظرسنجی (Survey Bot)

نمونه کامل پیاده‌سازی فرم ثبت‌نام چندمرحله‌ای با `StatesGroup`:

```python
import asyncio
import logging

from aiosplus import Bot, Dispatcher, F, MemoryStorage, State, StatesGroup
from aiosplus.filters import Command, StateFilter
from aiosplus.fsm.context import FSMContext
from aiosplus.types import Message, ReplyKeyboardRemove
from aiosplus.utils import ReplyKeyboardBuilder

logging.basicConfig(level=logging.INFO)

bot = Bot(token="YOUR_BOT_TOKEN")
dp = Dispatcher(storage=MemoryStorage())


class Registration(StatesGroup):
    full_name = State()
    age = State()
    gender = State()


@dp.message(Command("cancel"), StateFilter("*"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("عملیاتی برای لغو وجود ندارد.")
        return
    await state.clear()
    await message.answer("ثبت‌نام لغو شد.", reply_markup=ReplyKeyboardRemove())


@dp.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext) -> None:
    await state.set_state(Registration.full_name)
    await message.answer("لطفاً نام و نام خانوادگی خود را وارد کنید:")


@dp.message(StateFilter(Registration.full_name))
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(full_name=message.text)
    await state.set_state(Registration.age)
    await message.answer("سن خود را به عدد وارد کنید:")


@dp.message(StateFilter(Registration.age))
async def process_age(message: Message, state: FSMContext) -> None:
    if not message.text or not message.text.isdigit():
        await message.answer("لطفاً سن را به عدد وارد کنید:")
        return

    await state.update_data(age=int(message.text))
    await state.set_state(Registration.gender)

    builder = ReplyKeyboardBuilder()
    builder.button(text="مرد")
    builder.button(text="زن")
    builder.adjust(2)

    await message.answer(
        "جنسیت خود را انتخاب کنید:",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )


@dp.message(StateFilter(Registration.gender), F.text.in_(["مرد", "زن"]))
async def process_gender(message: Message, state: FSMContext) -> None:
    await state.update_data(gender=message.text)
    data = await state.get_data()

    await message.answer(
        f"✅ ثبت‌نام شما با موفقیت تکمیل شد:\n\n"
        f"👤 نام: {data.get('full_name')}\n"
        f"🎂 سن: {data.get('age')}\n"
        f"⚧ جنسیت: {data.get('gender')}",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.clear()


async def main() -> None:
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
```
