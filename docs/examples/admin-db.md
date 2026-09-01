# ربات ادمین و دیتابیس (Admin & Database)

نمونه اتصال به دیتابیس SQLite برای ذخیره کاربران و پنل اختصاصی ادمین:

```python
import asyncio
import logging
import sqlite3

from aiosplus import Bot, Dispatcher, F
from aiosplus.filters import Command, CommandStart
from aiosplus.types import CallbackQuery, Message
from aiosplus.utils import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN"
ADMIN_ID = 12345678  # شناسه کاربری ادمین

bot = Bot(token=TOKEN)
dp = Dispatcher()


class Database:
    def __init__(self, db_path: str = "users.db") -> None:
        self.conn = sqlite3.connect(db_path)
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    username TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add_user(self, user_id: int, first_name: str, username: str | None) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO users (user_id, first_name, username) VALUES (?, ?, ?)",
                (user_id, first_name, username),
            )

    def count_users(self) -> int:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        row = cursor.fetchone()
        return row[0] if row else 0


db = Database()


@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    if message.from_user:
        db.add_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username,
        )
    await message.answer("سلام! اطلاعات شما با موفقیت در دیتابیس ثبت شد.")


@dp.message(Command("admin"), F.from_user.id == ADMIN_ID)
async def on_admin(message: Message) -> None:
    total = db.count_users()
    builder = InlineKeyboardBuilder()
    builder.button(text="📊 مشاهده آمار", callback_data="admin:stats")
    await message.answer(
        f"👑 پنل ادمین:\n👥 کل کاربران ثبت‌شده: {total} نفر",
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(F.data == "admin:stats", F.from_user.id == ADMIN_ID)
async def on_stats_click(callback: CallbackQuery) -> None:
    total = db.count_users()
    await callback.answer(f"آمار دقیق: {total} کاربر فعال", show_alert=True)


async def main() -> None:
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
```
