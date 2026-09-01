import pytest

from aiosplus.dispatcher.router import Router
from aiosplus.filters import F
from aiosplus.types import (
    Animation,
    Chat,
    Contact,
    Document,
    Location,
    Message,
    PhotoSize,
    Sticker,
    Video,
    VideoNote,
    Voice,
)
from aiosplus.utils.formatting import (
    blockquote,
    bold,
    code,
    italic,
    link,
    pre,
    spoiler,
    strikethrough,
    underline,
)
from aiosplus.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


@pytest.mark.asyncio
async def test_message_content_type_properties() -> None:
    chat = Chat(id=1, type="private")

    # photo message
    msg_photo = Message(
        message_id=1,
        date=1,
        chat=chat,
        photo=[PhotoSize(file_id="p", file_unique_id="up", width=1, height=1)],
    )
    assert msg_photo.content_type == "photo"

    # audio message
    msg_audio = Message(
        message_id=2,
        date=1,
        chat=chat,
        audio=None,
        voice=Voice(file_id="v", file_unique_id="uv", duration=1),
    )
    assert msg_audio.content_type == "voice"

    # doc message
    msg_doc = Message(
        message_id=3, date=1, chat=chat, document=Document(file_id="d", file_unique_id="ud")
    )
    assert msg_doc.content_type == "document"

    # video message
    msg_vid = Message(
        message_id=4,
        date=1,
        chat=chat,
        video=Video(file_id="vd", file_unique_id="uvd", width=1, height=1, duration=1),
    )
    assert msg_vid.content_type == "video"

    # video_note message
    msg_vn = Message(
        message_id=5,
        date=1,
        chat=chat,
        video_note=VideoNote(file_id="vn", file_unique_id="uvn", length=1, duration=1),
    )
    assert msg_vn.content_type == "video_note"

    # animation message
    msg_an = Message(
        message_id=6,
        date=1,
        chat=chat,
        animation=Animation(file_id="an", file_unique_id="uan", width=1, height=1, duration=1),
    )
    assert msg_an.content_type == "animation"

    # sticker message
    msg_stk = Message(
        message_id=7,
        date=1,
        chat=chat,
        sticker=Sticker(
            file_id="s", file_unique_id="us", width=1, height=1, is_animated=False, is_video=False
        ),
    )
    assert msg_stk.content_type == "sticker"

    # contact message
    msg_cnt = Message(
        message_id=8, date=1, chat=chat, contact=Contact(phone_number="1", first_name="A")
    )
    assert msg_cnt.content_type == "contact"

    # location message
    msg_loc = Message(
        message_id=9, date=1, chat=chat, location=Location(latitude=1.0, longitude=1.0)
    )
    assert msg_loc.content_type == "location"

    # title change message
    msg_title = Message(message_id=10, date=1, chat=chat, new_chat_title="New Title")
    assert msg_title.content_type == "new_chat_title"

    # photo change message
    msg_new_photo = Message(
        message_id=11,
        date=1,
        chat=chat,
        new_chat_photo=[PhotoSize(file_id="p", file_unique_id="up", width=1, height=1)],
    )
    assert msg_new_photo.content_type == "new_chat_photo"

    # unknown message
    msg_unknown = Message(message_id=12, date=1, chat=chat)
    assert msg_unknown.content_type == "unknown"


@pytest.mark.asyncio
async def test_formatting_markdown_coverage() -> None:
    assert bold("txt", parse_mode="MarkdownV2") == "*txt*"
    assert italic("txt", parse_mode="MarkdownV2") == "_txt_"
    assert underline("txt", parse_mode="MarkdownV2") == "__txt__"
    assert strikethrough("txt", parse_mode="MarkdownV2") == "~txt~"
    assert spoiler("txt", parse_mode="MarkdownV2") == "||txt||"
    assert code("txt", parse_mode="MarkdownV2") == "`txt`"
    assert "```\ntxt\n```" == pre("txt", parse_mode="MarkdownV2")
    assert "```python\ntxt\n```" == pre("txt", language="python", parse_mode="MarkdownV2")
    assert (
        link("title", "https://example.com", parse_mode="MarkdownV2")
        == "[title](https://example.com)"
    )
    assert blockquote("line1\nline2", parse_mode="MarkdownV2") == ">line1\n>line2"
    assert (
        blockquote("line1\nline2", expandable=True, parse_mode="MarkdownV2") == "**>line1\n**>line2"
    )


@pytest.mark.asyncio
async def test_keyboard_builder_edge_cases() -> None:
    # Empty builder
    inline_empty = InlineKeyboardBuilder().as_markup()
    assert inline_empty.inline_keyboard == []

    reply_empty = ReplyKeyboardBuilder().as_markup()
    assert reply_empty.keyboard == []

    # Default sizes
    ikb = InlineKeyboardBuilder()
    ikb.button(text="A", callback_data="a")
    ikb.button(text="B", callback_data="b")
    markup_default = ikb.as_markup()
    assert len(markup_default.inline_keyboard) == 2

    # String buttons in ReplyKeyboardBuilder
    rkb = ReplyKeyboardBuilder()
    rkb.add("Option 1", "Option 2")
    assert len(rkb.as_markup().keyboard) == 2


@pytest.mark.asyncio
async def test_router_edge_cases() -> None:
    r1 = Router(name="R1")
    r2 = Router(name="R2")
    r1.include_router(r2)

    with pytest.raises(ValueError, match="Cannot include router into itself"):
        r1.include_router(r1)

    with pytest.raises(ValueError, match="already included"):
        r1.include_router(r2)


@pytest.mark.asyncio
async def test_magic_filter_advanced_operators() -> None:
    msg = Message(message_id=1, date=1, chat=Chat(id=1, type="private"), text="HelloWorld")

    assert await (F.text.in_(["HelloWorld", "Other"]))(msg) is True
    assert await (F.text.endswith("World"))(msg) is True
    assert await (F.text.func(lambda t: len(t) == 10))(msg) is True
    assert await (F.text.regexp(r"^Hello\w+"))(msg) is True
    assert await ((F.text == "Wrong") | (F.text == "HelloWorld"))(msg) is True
