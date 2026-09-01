from pathlib import Path

from aiosplus.enums import ChatType, MessageEntityType
from aiosplus.types import (
    Animation,
    Audio,
    BotCommand,
    BotCommandScopeChat,
    BotCommandScopeDefault,
    CallbackQuery,
    Chat,
    Contact,
    Document,
    File,
    ForceReply,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
    InputMediaPhoto,
    KeyboardButton,
    Location,
    MaskPosition,
    Message,
    PhotoSize,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Sticker,
    StickerSet,
    Update,
    User,
    UserProfilePhotos,
    WebhookInfo,
)


def test_user_model() -> None:
    user_data = {
        "id": 123456789,
        "is_bot": False,
        "first_name": "Ali",
        "last_name": "Rezaei",
        "username": "ali_rezaei",
        "language_code": "fa",
    }
    user = User.model_validate(user_data)
    assert user.id == 123456789
    assert user.is_bot is False
    assert user.full_name == "Ali Rezaei"
    assert user.mention == "@ali_rezaei"


def test_chat_model() -> None:
    chat_data = {
        "id": 987654321,
        "type": "supergroup",
        "title": "پایتون دولوپرز",
        "username": "python_devs",
    }
    chat = Chat.model_validate(chat_data)
    assert chat.id == 987654321
    assert chat.type == ChatType.SUPERGROUP
    assert chat.full_name == "پایتون دولوپرز"


def test_message_deserialization() -> None:
    raw_message = {
        "message_id": 42,
        "date": 1710000000,
        "from": {
            "id": 111,
            "is_bot": False,
            "first_name": "سارا",
        },
        "chat": {
            "id": 222,
            "type": "private",
            "first_name": "سارا",
        },
        "text": "/start hello",
        "entities": [
            {
                "type": "bot_command",
                "offset": 0,
                "length": 6,
            }
        ],
        "reply_markup": {"inline_keyboard": [[{"text": "کلیک کنید", "callback_data": "btn_1"}]]},
    }
    msg = Message.model_validate(raw_message)
    assert msg.message_id == 42
    assert msg.from_user is not None
    assert msg.from_user.first_name == "سارا"
    assert msg.chat.id == 222
    assert msg.text == "/start hello"
    assert msg.entities is not None
    assert msg.entities[0].type == MessageEntityType.BOT_COMMAND
    assert msg.reply_markup is not None
    assert msg.reply_markup.inline_keyboard[0][0].callback_data == "btn_1"
    assert msg.content_type == "text"


def test_update_and_callback_query() -> None:
    raw_update = {
        "update_id": 1001,
        "callback_query": {
            "id": "cb_999",
            "from": {
                "id": 111,
                "is_bot": False,
                "first_name": "حسین",
            },
            "data": "action:confirm",
            "message": {
                "message_id": 50,
                "date": 1710000100,
                "chat": {
                    "id": 111,
                    "type": "private",
                    "first_name": "حسین",
                },
                "text": "آیا مطمئن هستید؟",
            },
        },
    }
    update = Update.model_validate(raw_update)
    assert update.update_id == 1001
    assert update.event_type == "callback_query"
    assert isinstance(update.event, CallbackQuery)
    assert update.event.id == "cb_999"
    assert update.event.data == "action:confirm"
    assert update.event.from_user.first_name == "حسین"
    assert update.event.message is not None
    assert update.event.message.text == "آیا مطمئن هستید؟"


def test_keyboards_serialization() -> None:
    inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="سایت", url="https://splus.ir"),
                InlineKeyboardButton(text="منو", callback_data="menu"),
            ]
        ]
    )
    dumped_inline = inline_kb.model_dump(exclude_none=True)
    assert dumped_inline["inline_keyboard"][0][0]["url"] == "https://splus.ir"
    assert dumped_inline["inline_keyboard"][0][1]["callback_data"] == "menu"

    reply_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="ارسال شماره", request_contact=True),
                KeyboardButton(text="ارسال موقعیت", request_location=True),
            ]
        ],
        resize_keyboard=True,
    )
    dumped_reply = reply_kb.model_dump(exclude_none=True)
    assert dumped_reply["resize_keyboard"] is True
    assert dumped_reply["keyboard"][0][0]["request_contact"] is True

    remove_kb = ReplyKeyboardRemove()
    assert remove_kb.model_dump(exclude_none=True)["remove_keyboard"] is True

    force_reply = ForceReply(input_field_placeholder="نام خود را وارد کنید")
    assert force_reply.model_dump(exclude_none=True)["force_reply"] is True


def test_media_models() -> None:
    photo = PhotoSize(file_id="p123", file_unique_id="u123", width=800, height=600, file_size=1024)
    assert photo.width == 800

    doc = Document(
        file_id="d123", file_unique_id="ud123", file_name="book.pdf", mime_type="application/pdf"
    )
    assert doc.file_name == "book.pdf"

    audio = Audio(
        file_id="a123", file_unique_id="ua123", duration=180, performer="خواننده", title="آهنگ"
    )
    assert audio.title == "آهنگ"

    contact = Contact(phone_number="+989120000000", first_name="رضا")
    assert contact.phone_number == "+989120000000"

    location = Location(latitude=35.6892, longitude=51.3890)
    assert location.latitude == 35.6892

    file_obj = File(
        file_id="f123", file_unique_id="uf123", file_path="documents/test.pdf", file_size=2048
    )
    assert file_obj.file_path == "documents/test.pdf"

    anim = Animation(file_id="anim1", file_unique_id="uanim1", width=320, height=240, duration=5)
    assert anim.duration == 5

    user_photos = UserProfilePhotos(total_count=1, photos=[[photo]])
    assert user_photos.total_count == 1

    input_media = InputMediaPhoto(media="p123", caption="تست کپشن")
    assert input_media.type == "photo"


def test_commands_and_webhook_info() -> None:
    cmd = BotCommand(command="help", description="نمایش راهنما")
    assert cmd.command == "help"

    scope_default = BotCommandScopeDefault()
    assert scope_default.type == "default"

    scope_chat = BotCommandScopeChat(chat_id=12345)
    assert scope_chat.chat_id == 12345

    webhook = WebhookInfo(
        url="https://example.com/webhook", has_custom_certificate=False, pending_update_count=0
    )
    assert webhook.url == "https://example.com/webhook"

    mask = MaskPosition(point="eyes", x_shift=0.0, y_shift=0.0, scale=1.0)
    sticker = Sticker(
        file_id="stk1",
        file_unique_id="ustk1",
        width=512,
        height=512,
        is_animated=False,
        is_video=False,
        mask_position=mask,
    )
    sticker_set = StickerSet(name="set1", title="ست یک", stickers=[sticker])
    assert sticker_set.name == "set1"


def test_input_file(tmp_path: Path) -> None:
    test_file = tmp_path / "sample.txt"
    test_file.write_text("Soroush Plus Test File Content", encoding="utf-8")

    input_file = InputFile(test_file)
    assert input_file.filename == "sample.txt"
    assert input_file.content_type == "text/plain"
    assert input_file.read_bytes() == b"Soroush Plus Test File Content"

    # From bytes
    input_bytes = InputFile(b"binary data", filename="data.bin")
    assert input_bytes.filename == "data.bin"
    assert input_bytes.read_bytes() == b"binary data"

    # Remote file_id
    input_remote = InputFile("AgACAgIAAxkBAAI...")
    assert input_remote.file_id == "AgACAgIAAxkBAAI..."
