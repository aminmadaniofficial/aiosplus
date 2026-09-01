"""نمونه فرم ثبت‌نام چندمرحله‌ای با استفاده از ماشین وضعیت (FSM).

Multi-step Form Survey Bot with FSM using aiosplus.
"""

import asyncio
import logging

from aiosplus import Bot, Dispatcher, F, MemoryStorage, State, StatesGroup
from aiosplus.filters import Command, StateFilter
from aiosplus.fsm.context import FSMContext
from aiosplus.types import Message, ReplyKeyboardRemove
from aiosplus.utils import ReplyKeyboardBuilder

logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = Bot(token=TOKEN)

# استفاده از MemoryStorage برای نگهداری وضعیت‌ها در حافظه
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


# تعریف مراحل فرم ثبت‌نام
class RegistrationForm(StatesGroup):
    full_name = State()
    age = State()
    gender = State()


@dp.message(Command("cancel"), StateFilter("*"))
async def cmd_cancel(message: Message, state: FSMContext) -> None:
    """لغو فرآیند ثبت‌نام در هر مرحله."""
    current_state = await state.get_state()
    if current_state is None:
        await message.answer("هیچ عملیاتی برای لغو وجود ندارد.")
        return

    await state.clear()
    await message.answer("ثبت‌نام با موفقیت لغو شد.", reply_markup=ReplyKeyboardRemove())


@dp.message(Command("register"))
async def cmd_register(message: Message, state: FSMContext) -> None:
    """شروع مرحله اول ثبت‌نام."""
    await state.set_state(RegistrationForm.full_name)
    await message.answer("لطفاً نام و نام‌خانوادگی خود را وارد کنید:")


@dp.message(StateFilter(RegistrationForm.full_name))
async def process_name(message: Message, state: FSMContext) -> None:
    """دریافت نام و انتقال به مرحله سن."""
    if not message.text or len(message.text) < 3:
        await message.answer("نام وارد شده معتبر نیست. لطفاً مجدداً وارد کنید:")
        return

    await state.update_data(full_name=message.text)
    await state.set_state(RegistrationForm.age)
    await message.answer("سن خود را به صورت عدد وارد کنید:")


@dp.message(StateFilter(RegistrationForm.age))
async def process_age(message: Message, state: FSMContext) -> None:
    """دریافت سن و انتقال به مرحله جنسیت با کیبورد انتخابی."""
    if not message.text or not message.text.isdigit():
        await message.answer("لطفاً سن خود را فقط با ارقام وارد کنید:")
        return

    await state.update_data(age=int(message.text))
    await state.set_state(RegistrationForm.gender)

    builder = ReplyKeyboardBuilder()
    builder.button(text="مرد")
    builder.button(text="زن")
    builder.adjust(2)

    await message.answer(
        "جنسیت خود را انتخاب کنید:",
        reply_markup=builder.as_markup(resize_keyboard=True, one_time_keyboard=True),
    )


@dp.message(StateFilter(RegistrationForm.gender), F.text.in_(["مرد", "زن"]))
async def process_gender(message: Message, state: FSMContext) -> None:
    """پایان ثبت‌نام و نمایش اطلاعات ثبت‌شده."""
    await state.update_data(gender=message.text)
    data = await state.get_data()

    summary = (
        "✅ ثبت‌نام شما با موفقیت تکمیل شد:\n\n"
        f"👤 نام: {data.get('full_name')}\n"
        f"🎂 سن: {data.get('age')}\n"
        f"⚧ جنسیت: {data.get('gender')}"
    )

    await message.answer(summary, reply_markup=ReplyKeyboardRemove())
    await state.clear()


async def main() -> None:
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
