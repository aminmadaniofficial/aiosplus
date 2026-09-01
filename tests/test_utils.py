import pytest

from aiosplus.bot.bot import Bot
from aiosplus.dispatcher.dispatcher import Dispatcher
from aiosplus.types import Message
from aiosplus.utils.formatting import (
    blockquote,
    bold,
    code,
    escape_html,
    escape_md,
    italic,
    link,
    pre,
    spoiler,
    strikethrough,
    underline,
)
from aiosplus.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiosplus.utils.webhook import SimpleWebhookHandler


def test_inline_keyboard_builder() -> None:
    builder = InlineKeyboardBuilder()
    builder.button(text="Btn 1", callback_data="cb_1")
    builder.button(text="Btn 2", callback_data="cb_2")
    builder.button(text="Btn 3", url="https://splus.ir")
    builder.adjust(2, 1)

    markup = builder.as_markup()
    assert len(markup.inline_keyboard) == 2
    assert len(markup.inline_keyboard[0]) == 2
    assert len(markup.inline_keyboard[1]) == 1
    assert markup.inline_keyboard[0][0].text == "Btn 1"
    assert markup.inline_keyboard[1][0].url == "https://splus.ir"


def test_reply_keyboard_builder() -> None:
    builder = ReplyKeyboardBuilder()
    builder.button(text="ارسال شماره", request_contact=True)
    builder.button(text="ارسال موقعیت", request_location=True)
    builder.button(text="لغو")
    builder.adjust(2, 1)

    markup = builder.as_markup(resize_keyboard=True, input_field_placeholder="یک گزینه انتخاب کنید")
    assert len(markup.keyboard) == 2
    assert len(markup.keyboard[0]) == 2
    assert len(markup.keyboard[1]) == 1
    assert markup.resize_keyboard is True
    assert markup.input_field_placeholder == "یک گزینه انتخاب کنید"
    assert markup.keyboard[0][0].request_contact is True


def test_formatting_utils() -> None:
    raw = "Hello <world> & friends *test* _italic_!"
    assert "&lt;world&gt;" in escape_html(raw)
    assert "\\*test\\*" in escape_md(raw)

    assert bold("Hello", parse_mode="HTML") == "<b>Hello</b>"
    assert bold("Hello", parse_mode="MarkdownV2") == "*Hello*"

    assert italic("Hi", parse_mode="HTML") == "<i>Hi</i>"
    assert underline("Under", parse_mode="HTML") == "<u>Under</u>"
    assert strikethrough("Del", parse_mode="HTML") == "<s>Del</s>"
    assert "tg-spoiler" in spoiler("Secret", parse_mode="HTML")
    assert code("x = 10", parse_mode="HTML") == "<code>x = 10</code>"
    assert "language-python" in pre("print(1)", language="python", parse_mode="HTML")
    assert '<a href="https://example.com">Site</a>' == link(
        "Site", "https://example.com", parse_mode="HTML"
    )
    assert "<blockquote>Quote</blockquote>" == blockquote("Quote", parse_mode="HTML")


@pytest.mark.asyncio
async def test_simple_webhook_handler() -> None:
    dp = Dispatcher()
    bot = Bot("123:ABC")
    events: list[str] = []

    @dp.message()
    async def echo(msg: Message) -> None:
        if msg.text:
            events.append(msg.text)

    handler = SimpleWebhookHandler(dispatcher=dp, bot=bot)
    raw_payload = {
        "update_id": 1,
        "message": {
            "message_id": 100,
            "date": 1710000000,
            "chat": {"id": 1, "type": "private"},
            "text": "Webhook text payload",
        },
    }
    handled = await handler.feed_raw_update(raw_payload)
    assert handled is True
    assert events == ["Webhook text payload"]
