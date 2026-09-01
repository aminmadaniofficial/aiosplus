from pathlib import Path

import httpx
import pytest

from aiosplus.bot.bot import Bot
from aiosplus.client.session import AioSplusSession
from aiosplus.enums import ChatAction, ParseMode
from aiosplus.types import (
    BotCommand,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
    Message,
)


@pytest.mark.asyncio
async def test_bot_get_me() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://api.splus.ir/bot123:TOKEN/getMe"
        return httpx.Response(
            200,
            json={
                "ok": True,
                "result": {
                    "id": 99999,
                    "is_bot": True,
                    "first_name": "TestBot",
                    "username": "test_bot",
                },
            },
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        session = AioSplusSession(client=mock_client)
        bot = Bot(token="123:TOKEN", session=session)
        me = await bot.get_me()
        assert me.id == 99999
        assert me.is_bot is True
        assert me.first_name == "TestBot"


@pytest.mark.asyncio
async def test_bot_send_message_and_reply_helpers() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://api.splus.ir/bot123:TOKEN/sendMessage"
        return httpx.Response(
            200,
            json={
                "ok": True,
                "result": {
                    "message_id": 101,
                    "date": 1710000000,
                    "chat": {"id": 12345, "type": "private", "first_name": "User"},
                    "text": "Response text",
                },
            },
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        session = AioSplusSession(client=mock_client)
        bot = Bot(token="123:TOKEN", session=session, default_parse_mode=ParseMode.HTML)
        msg = await bot.send_message(
            chat_id=12345,
            text="Hello!",
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[InlineKeyboardButton(text="Click", callback_data="btn")]]
            ),
        )
        assert isinstance(msg, Message)
        assert msg.message_id == 101
        assert msg.text == "Response text"

        # Test message.answer convenience method
        reply_msg = await msg.answer("Answer back")
        assert reply_msg.message_id == 101

        # Test message.reply convenience method
        reply_to = await msg.reply("Direct reply")
        assert reply_to.message_id == 101


@pytest.mark.asyncio
async def test_bot_send_photo_and_multipart(tmp_path: Path) -> None:
    test_img = tmp_path / "test.png"
    test_img.write_bytes(b"\x89PNG\r\n\x1a\nfakeimagebytes")

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://api.splus.ir/bot123:TOKEN/sendPhoto"
        assert "multipart/form-data" in request.headers.get("content-type", "")
        return httpx.Response(
            200,
            json={
                "ok": True,
                "result": {
                    "message_id": 102,
                    "date": 1710000000,
                    "chat": {"id": 12345, "type": "private"},
                    "photo": [
                        {"file_id": "p1", "file_unique_id": "up1", "width": 100, "height": 100}
                    ],
                    "caption": "Photo caption",
                },
            },
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        session = AioSplusSession(client=mock_client)
        bot = Bot(token="123:TOKEN", session=session)
        msg = await bot.send_photo(
            chat_id=12345,
            photo=InputFile(test_img),
            caption="Photo caption",
        )
        assert msg.message_id == 102
        assert msg.caption == "Photo caption"


@pytest.mark.asyncio
async def test_bot_get_updates() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://api.splus.ir/bot123:TOKEN/getUpdates"
        return httpx.Response(
            200,
            json={
                "ok": True,
                "result": [
                    {
                        "update_id": 1,
                        "message": {
                            "message_id": 10,
                            "date": 1710000000,
                            "chat": {"id": 12345, "type": "private"},
                            "text": "Update message",
                        },
                    }
                ],
            },
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        session = AioSplusSession(client=mock_client)
        bot = Bot(token="123:TOKEN", session=session)
        updates = await bot.get_updates(offset=0, timeout=10)
        assert len(updates) == 1
        assert updates[0].update_id == 1
        assert updates[0].message is not None
        assert updates[0].message.text == "Update message"


@pytest.mark.asyncio
async def test_bot_webhook_and_commands() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        if "setWebhook" in url_str:
            return httpx.Response(200, json={"ok": True, "result": True})
        if "deleteWebhook" in url_str:
            return httpx.Response(200, json={"ok": True, "result": True})
        if "setMyCommands" in url_str:
            return httpx.Response(200, json={"ok": True, "result": True})
        if "getMyCommands" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": [{"command": "start", "description": "Start the bot"}],
                },
            )
        if "sendChatAction" in url_str:
            return httpx.Response(200, json={"ok": True, "result": True})
        return httpx.Response(404, json={"ok": False, "description": "Not Found"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        session = AioSplusSession(client=mock_client)
        bot = Bot(token="123:TOKEN", session=session)

        assert await bot.set_webhook("https://mybot.com/webhook") is True
        assert await bot.delete_webhook() is True
        assert await bot.set_my_commands([BotCommand(command="start", description="Start")]) is True
        cmds = await bot.get_my_commands()
        assert len(cmds) == 1
        assert cmds[0].command == "start"
        assert await bot.send_chat_action(12345, ChatAction.TYPING) is True
