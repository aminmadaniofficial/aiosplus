import httpx
import pytest

from aiosplus.bot.bot import Bot
from aiosplus.client.session import AioSplusSession
from aiosplus.dispatcher.dispatcher import Dispatcher
from aiosplus.filters import Command, StateFilter
from aiosplus.fsm.context import FSMContext
from aiosplus.fsm.state import State, StatesGroup
from aiosplus.fsm.storage.memory import MemoryStorage
from aiosplus.types import Chat, Message, Update, User


class UserRegistration(StatesGroup):
    name = State()
    age = State()
    phone = State()


def test_states_group_naming() -> None:
    assert UserRegistration.name.state == "UserRegistration:name"
    assert UserRegistration.age.state == "UserRegistration:age"
    assert UserRegistration.phone.state == "UserRegistration:phone"
    assert str(UserRegistration.name) == "UserRegistration:name"
    assert UserRegistration.name == "UserRegistration:name"


@pytest.mark.asyncio
async def test_memory_storage_and_context() -> None:
    storage = MemoryStorage()
    bot = Bot("123:ABC")
    dp = Dispatcher(storage=storage)
    ctx = dp.get_fsm_context(bot, chat_id=123, user_id=456)
    assert ctx is not None

    # Initial state
    assert await ctx.get_state() is None
    assert await ctx.get_data() == {}

    # Set state
    await ctx.set_state(UserRegistration.name)
    assert await ctx.get_state() == "UserRegistration:name"

    # Update data
    await ctx.update_data(first_name="Reza")
    await ctx.update_data(last_name="Ahmadi")
    data = await ctx.get_data()
    assert data == {"first_name": "Reza", "last_name": "Ahmadi"}

    # Clear
    await ctx.clear()
    assert await ctx.get_state() is None
    assert await ctx.get_data() == {}
    await storage.close()


@pytest.mark.asyncio
async def test_fsm_dispatcher_survey_flow() -> None:
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    flow_steps: list[str] = []

    @dp.message(Command("register"))
    async def start_reg(_message: Message, state: FSMContext) -> None:
        flow_steps.append("start_reg")
        await state.set_state(UserRegistration.name)

    @dp.message(StateFilter(UserRegistration.name))
    async def process_name(message: Message, state: FSMContext) -> None:
        flow_steps.append(f"got_name:{message.text}")
        await state.update_data(name=message.text)
        await state.set_state(UserRegistration.age)

    @dp.message(StateFilter(UserRegistration.age))
    async def process_age(message: Message, state: FSMContext) -> None:
        flow_steps.append(f"got_age:{message.text}")
        await state.update_data(age=message.text)
        user_data = await state.get_data()
        flow_steps.append(f"completed:{user_data['name']}_{user_data['age']}")
        await state.clear()

    transport = httpx.MockTransport(
        lambda _req: httpx.Response(200, json={"ok": True, "result": True})
    )
    async with httpx.AsyncClient(transport=transport) as mock_client:
        bot = Bot("123:ABC", session=AioSplusSession(client=mock_client))
        user = User(id=10, is_bot=False, first_name="Ali")
        chat = Chat(id=10, type="private")

        # Step 1: /register
        up1 = Update(
            update_id=1,
            message=Message(message_id=1, date=100, chat=chat, from_user=user, text="/register"),
        )
        await dp.feed_update(bot, up1)
        assert flow_steps == ["start_reg"]

        # Step 2: send name "Ali"
        up2 = Update(
            update_id=2,
            message=Message(message_id=2, date=101, chat=chat, from_user=user, text="Ali"),
        )
        await dp.feed_update(bot, up2)
        assert flow_steps == ["start_reg", "got_name:Ali"]

        # Step 3: send age "25"
        up3 = Update(
            update_id=3,
            message=Message(message_id=3, date=102, chat=chat, from_user=user, text="25"),
        )
        await dp.feed_update(bot, up3)
        assert flow_steps == ["start_reg", "got_name:Ali", "got_age:25", "completed:Ali_25"]

        # Verify state is cleared
        ctx = dp.get_fsm_context(bot, chat_id=10, user_id=10)
        assert ctx is not None
        assert await ctx.get_state() is None
        assert await ctx.get_data() == {}
