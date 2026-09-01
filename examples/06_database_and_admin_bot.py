"""نمونه ربات کاربردی پنل مدیریت و ذخیره‌سازی اطلاعات کاربران در دیتابیس SQLite.

Practical Bot with SQLite Database & Admin Panel using aiosplus.
"""

import asyncio
import logging
import sqlite3

from aiosplus import Bot, Dispatcher, F
from aiosplus.filters import Command, CommandStart
from aiosplus.types import CallbackQuery, Message
from aiosplus.utils import InlineKeyboardBuilder

logging.basicConfig(level=logging.INFO)

TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_ID = 12345678  # شناسه کاربری ادمین ربات

bot = Bot(token=TOKEN)
dp = Dispatcher()


# ساختار ساده پایگاه داده محلی
class Database:
    def __init__(self, db_path: str = "bot_users.db") -> None:
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self) -> None:
        with self.conn:
            self.conn.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    username TEXT,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

    def add_user(self, user_id: int, first_name: str, username: str | None) -> None:
        with self.conn:
            self.conn.execute(
                "INSERT OR IGNORE INTO users (user_id, first_name, username) VALUES (?, ?, ?)",
                (user_id, first_name, username),
            )

    def get_users_count(self) -> int:
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        row = cursor.fetchone()
        return row[0] if row else 0

    def get_all_user_ids(self) -> list[int]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT user_id FROM users")
        return [row[0] for row in cursor.fetchall()]


db = Database()


@dp.message(CommandStart())
async def on_start(message: Message) -> None:
    """ثبت‌نام خودکار کاربر در پایگاه داده با شروع ربات."""
    if message.from_user:
        db.add_user(
            user_id=message.from_user.id,
            first_name=message.from_user.first_name,
            username=message.from_user.username,
        )

    builder = InlineKeyboardBuilder()
    builder.button(text="ℹ️ درباره سروش‌پلاس", callback_data="about")
    builder.button(text="📞 پشتیبانی", callback_data="support")
    builder.adjust(2)

    await message.answer(
        "سلام! به ربات خوش آمدید.\nاطلاعات شما در پایگاه‌داده ذخیره شد.",
        reply_markup=builder.as_markup(),
    )


@dp.message(Command("admin"), F.from_user.id == ADMIN_ID)
async def admin_panel(message: Message) -> None:
    """پنل مدیریت اختصاصی برای ادمین ربات."""
    total_users = db.get_users_count()

    builder = InlineKeyboardBuilder()
    builder.button(text="📊 آمار تفکیکی", callback_data="admin:stats")
    builder.button(text="📢 ارسال پیام همگانی", callback_data="admin:broadcast_prompt")
    builder.adjust(1, 1)

    await message.answer(
        f"👑 پنل مدیریت ربات:\n\n👥 کل اعضای ثبت‌شده: {total_users} نفر",
        reply_markup=builder.as_markup(),
    )


@dp.callback_query(F.data == "admin:stats", F.from_user.id == ADMIN_ID)
async def admin_stats_callback(callback: CallbackQuery) -> None:
    total_users = db.get_users_count()
    await callback.answer(f"تعداد دقیق کاربران فعال: {total_users}", show_alert=True)


@dp.callback_query(F.data == "about")
async def about_callback(callback: CallbackQuery) -> None:
    await callback.answer("توسعه یافته با فریم‌ورک aiosplus", show_alert=True)


async def main() -> None:
    await dp.start_polling(bot, drop_pending_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
