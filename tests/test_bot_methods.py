from pathlib import Path

import httpx
import pytest

from aiosplus.bot.bot import Bot
from aiosplus.client.session import AioSplusSession
from aiosplus.enums import ParseMode
from aiosplus.filters import CommandHelp, CommandStart
from aiosplus.middlewares.logging import LoggingMiddleware
from aiosplus.types import (
    Chat,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    InputFile,
    InputMediaPhoto,
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
        assert Bot.get_current() is bot
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
async def test_bot_all_media_methods() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        fake_msg = {
            "message_id": 200,
            "date": 1710000000,
            "chat": {"id": 12345, "type": "private"},
        }
        if "sendAudio" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {
                        **fake_msg,
                        "audio": {"file_id": "a1", "file_unique_id": "ua1", "duration": 120},
                    },
                },
            )
        if "sendDocument" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {**fake_msg, "document": {"file_id": "d1", "file_unique_id": "ud1"}},
                },
            )
        if "sendVideo" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {
                        **fake_msg,
                        "video": {
                            "file_id": "v1",
                            "file_unique_id": "uv1",
                            "width": 640,
                            "height": 480,
                            "duration": 60,
                        },
                    },
                },
            )
        if "sendAnimation" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {
                        **fake_msg,
                        "animation": {
                            "file_id": "an1",
                            "file_unique_id": "uan1",
                            "width": 320,
                            "height": 240,
                            "duration": 10,
                        },
                    },
                },
            )
        if "sendVoice" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {
                        **fake_msg,
                        "voice": {"file_id": "vo1", "file_unique_id": "uvo1", "duration": 30},
                    },
                },
            )
        if "sendVideoNote" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {
                        **fake_msg,
                        "video_note": {
                            "file_id": "vn1",
                            "file_unique_id": "uvn1",
                            "length": 240,
                            "duration": 15,
                        },
                    },
                },
            )
        if "sendLocation" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {**fake_msg, "location": {"latitude": 35.7, "longitude": 51.4}},
                },
            )
        if "sendContact" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {
                        **fake_msg,
                        "contact": {"phone_number": "+989123456789", "first_name": "Test"},
                    },
                },
            )
        if "sendSticker" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {
                        **fake_msg,
                        "sticker": {
                            "file_id": "s1",
                            "file_unique_id": "us1",
                            "width": 512,
                            "height": 512,
                            "is_animated": False,
                            "is_video": False,
                        },
                    },
                },
            )
        if "sendMediaGroup" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": [
                        {
                            **fake_msg,
                            "photo": [
                                {
                                    "file_id": "p1",
                                    "file_unique_id": "up1",
                                    "width": 100,
                                    "height": 100,
                                }
                            ],
                        }
                    ],
                },
            )
        if "getFile" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {
                        "file_id": "f1",
                        "file_unique_id": "uf1",
                        "file_path": "photos/f1.jpg",
                        "file_size": 1024,
                    },
                },
            )
        if "getUserProfilePhotos" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {
                        "total_count": 1,
                        "photos": [
                            [
                                {
                                    "file_id": "p1",
                                    "file_unique_id": "up1",
                                    "width": 100,
                                    "height": 100,
                                }
                            ]
                        ],
                    },
                },
            )
        if "getChat" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {"id": 12345, "type": "private", "first_name": "TestChat"},
                },
            )
        if "getStickerSet" in url_str:
            return httpx.Response(
                200,
                json={
                    "ok": True,
                    "result": {"name": "test_set", "title": "Test Set", "stickers": []},
                },
            )
        if (
            "pinChatMessage" in url_str
            or "unpinChatMessage" in url_str
            or "deleteMessage" in url_str
        ):
            return httpx.Response(200, json={"ok": True, "result": True})
        if (
            "editMessageText" in url_str
            or "editMessageCaption" in url_str
            or "editMessageMedia" in url_str
            or "editMessageReplyMarkup" in url_str
        ):
            return httpx.Response(200, json={"ok": True, "result": fake_msg})
        return httpx.Response(404, json={"ok": False, "description": "Not Found"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        session = AioSplusSession(client=mock_client)
        bot = Bot(token="123:TOKEN", session=session)

        # Audio, Doc, Video, Animation, Voice, VideoNote
        assert (await bot.send_audio(12345, "a1")).message_id == 200
        assert (await bot.send_document(12345, "d1")).message_id == 200
        assert (await bot.send_video(12345, "v1")).message_id == 200
        assert (await bot.send_animation(12345, "an1")).message_id == 200
        assert (await bot.send_voice(12345, "vo1")).message_id == 200
        assert (await bot.send_video_note(12345, "vn1")).message_id == 200
        assert (await bot.send_location(12345, 35.7, 51.4)).message_id == 200
        assert (await bot.send_contact(12345, "+989123456789", "Test")).message_id == 200
        assert (await bot.send_sticker(12345, "s1")).message_id == 200

        # MediaGroup
        mg = await bot.send_media_group(12345, [InputMediaPhoto(media="p1")])
        assert len(mg) == 1

        # File & Profiles & Chat
        file_obj = await bot.get_file("f1")
        assert file_obj.file_path == "photos/f1.jpg"

        prof = await bot.get_user_profile_photos(12345)
        assert prof.total_count == 1

        chat = await bot.get_chat(12345)
        assert chat.id == 12345

        stk_set = await bot.get_sticker_set("test_set")
        assert stk_set.name == "test_set"

        # Pins & Edits & Delete
        assert await bot.pin_chat_message(12345, 200) is True
        assert await bot.unpin_chat_message(12345, 200) is True
        assert await bot.delete_message(12345, 200) is True

        assert isinstance(await bot.edit_message_text("Edited", 12345, 200), Message)
        assert isinstance(await bot.edit_message_caption(12345, 200, caption="New Cap"), Message)
        assert isinstance(
            await bot.edit_message_media(InputMediaPhoto(media="p1"), 12345, 200), Message
        )
        assert isinstance(await bot.edit_message_reply_markup(12345, 200), Message)


@pytest.mark.asyncio
async def test_command_start_and_help_filters() -> None:
    filter_start = CommandStart(deep_link=r"ref_\d+")
    msg_valid = Message(
        message_id=1,
        date=1710000000,
        chat=Chat(id=1, type="private"),
        text="/start ref_12345",
    )
    res_valid = await filter_start(msg_valid)
    assert isinstance(res_valid, dict)
    assert res_valid["command"].deep_link == "ref_12345"

    msg_invalid = Message(
        message_id=2,
        date=1710000000,
        chat=Chat(id=1, type="private"),
        text="/start invalid_arg",
    )
    assert await filter_start(msg_invalid) is False

    filter_help = CommandHelp()
    msg_help = Message(
        message_id=3,
        date=1710000000,
        chat=Chat(id=1, type="private"),
        text="/help",
    )
    assert await filter_help(msg_help) is not False


@pytest.mark.asyncio
async def test_logging_middleware() -> None:
    middleware = LoggingMiddleware()
    called = False

    async def sample_handler(_event: object, _data: dict[str, object]) -> str:
        nonlocal called
        called = True
        return "done"

    result = await middleware(sample_handler, "test_event", {})
    assert result == "done"
    assert called is True
