from typing import Any

import httpx
import pytest

from aiosplus.bot.bot import Bot
from aiosplus.client.session import AioSplusSession
from aiosplus.dispatcher.dispatcher import Dispatcher
from aiosplus.dispatcher.router import Router
from aiosplus.enums import ChatType
from aiosplus.filters import (
    ChatTypeFilter,
    Command,
    CommandObject,
    F,
    Text,
)
from aiosplus.middlewares.base import BaseMiddleware, HandlerType
from aiosplus.types import (
    CallbackQuery,
    Chat,
    Message,
    Update,
    User,
)


@pytest.mark.asyncio
async def test_command_filter() -> None:
    filter_cmd = Command("start")
    msg = Message(
        message_id=1,
        date=1710000000,
        chat=Chat(id=10, type="private"),
        text="/start 123",
        from_user=User(id=1, is_bot=False, first_name="Tester"),
    )
    result = await filter_cmd(msg)
    assert isinstance(result, dict)
    assert "command" in result
    cmd_obj: CommandObject = result["command"]
    assert cmd_obj.command == "start"
    assert cmd_obj.args == "123"
    assert cmd_obj.prefix == "/"


@pytest.mark.asyncio
async def test_text_and_chat_type_filters() -> None:
    msg_private = Message(
        message_id=1,
        date=1710000000,
        chat=Chat(id=10, type="private"),
        text="Hello World",
    )
    filter_private = ChatTypeFilter(ChatType.PRIVATE)
    assert await filter_private(msg_private) is True

    filter_group = ChatTypeFilter(ChatType.GROUP)
    assert await filter_group(msg_private) is False

    filter_text_start = Text(startswith="Hello")
    assert await filter_text_start(msg_private) is True

    filter_text_end = Text(endswith="World")
    assert await filter_text_end(msg_private) is True


@pytest.mark.asyncio
async def test_magic_filter_f() -> None:
    msg = Message(
        message_id=10,
        date=1710000000,
        chat=Chat(id=10, type="private"),
        text="Order: 12345",
        from_user=User(id=99, is_bot=False, first_name="Ali"),
    )

    filter_eq = F.from_user.id == 99
    assert await filter_eq(msg) is True

    filter_wrong_id = F.from_user.id == 100
    assert await filter_wrong_id(msg) is False

    filter_text_starts = F.text.startswith("Order:")
    assert await filter_text_starts(msg) is True

    filter_and = (F.from_user.id == 99) & F.text.contains("12345")
    assert await filter_and(msg) is True

    filter_not = ~F.text.contains("NonExistent")
    assert await filter_not(msg) is True


@pytest.mark.asyncio
async def test_router_and_dispatcher_dispatch() -> None:
    dp = Dispatcher()
    router = Router()
    dp.include_router(router)

    handled_events: list[str] = []

    @router.message(Command("hello"))
    async def hello_handler(_message: Message, command: CommandObject) -> None:
        handled_events.append(f"hello:{command.command}")

    @router.callback_query(F.data == "click_me")
    async def callback_handler(callback: CallbackQuery) -> None:
        handled_events.append(f"callback:{callback.data}")

    transport = httpx.MockTransport(
        lambda _req: httpx.Response(200, json={"ok": True, "result": True})
    )
    async with httpx.AsyncClient(transport=transport) as mock_client:
        bot = Bot("123:ABC", session=AioSplusSession(client=mock_client))

        # Feed message update
        up1 = Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=1710000000,
                chat=Chat(id=1, type="private"),
                text="/hello",
            ),
        )
        handled1 = await dp.feed_update(bot, up1)
        assert handled1 is True
        assert handled_events == ["hello:hello"]

        # Feed callback update
        up2 = Update(
            update_id=2,
            callback_query=CallbackQuery(
                id="cb_1",
                from_user=User(id=1, is_bot=False, first_name="Tester"),
                data="click_me",
            ),
        )
        handled2 = await dp.feed_update(bot, up2)
        assert handled2 is True
        assert handled_events == ["hello:hello", "callback:click_me"]


@pytest.mark.asyncio
async def test_middleware_pipeline() -> None:
    dp = Dispatcher()
    log: list[str] = []

    class TestMiddleware(BaseMiddleware):
        async def __call__(
            self,
            handler: HandlerType,
            event: Any,
            data: dict[str, Any],
        ) -> Any:
            log.append("pre_middleware")
            res = await handler(event, data)
            log.append("post_middleware")
            return res

    dp.message.middleware(TestMiddleware())

    @dp.message(F.text == "ping")
    async def ping_handler(_message: Message) -> None:
        log.append("handler_ping")

    transport = httpx.MockTransport(
        lambda _req: httpx.Response(200, json={"ok": True, "result": True})
    )
    async with httpx.AsyncClient(transport=transport) as mock_client:
        bot = Bot("123:ABC", session=AioSplusSession(client=mock_client))
        up = Update(
            update_id=1,
            message=Message(
                message_id=1,
                date=1710000000,
                chat=Chat(id=1, type="private"),
                text="ping",
            ),
        )
        await dp.feed_update(bot, up)
        assert log == ["pre_middleware", "handler_ping", "post_middleware"]
