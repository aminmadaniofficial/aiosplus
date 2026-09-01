import pytest

from aiosplus.fsm.state import State
from aiosplus.fsm.storage.base import StorageKey
from aiosplus.fsm.storage.redis import RedisStorage


class FakeRedis:
    """In-memory mock for redis.asyncio client."""

    def __init__(self) -> None:
        self.store: dict[str, str] = {}
        self.closed = False

    async def get(self, key: str) -> str | None:
        return self.store.get(key)

    async def set(self, key: str, value: str, ex: int | None = None) -> None:
        del ex
        self.store[key] = value

    async def delete(self, key: str) -> None:
        self.store.pop(key, None)

    async def aclose(self) -> None:
        self.closed = True


@pytest.mark.asyncio
async def test_redis_storage_operations() -> None:
    fake_client = FakeRedis()
    storage = RedisStorage(redis=fake_client, key_prefix="test_fsm")
    key = StorageKey(bot_id=1, chat_id=100, user_id=200)

    # Initial state
    assert await storage.get_state(key) is None
    assert await storage.get_data(key) == {}

    # Set state as string and as State
    test_state = State("waiting_for_input", group_name="Survey")
    await storage.set_state(key, test_state)
    assert await storage.get_state(key) == "Survey:waiting_for_input"

    # Set data
    await storage.set_data(key, {"email": "user@splus.ir"})
    assert await storage.get_data(key) == {"email": "user@splus.ir"}

    # Update data
    updated = await storage.update_data(key, role="admin")
    assert updated == {"email": "user@splus.ir", "role": "admin"}
    assert await storage.get_data(key) == {"email": "user@splus.ir", "role": "admin"}

    # Clear state and data
    await storage.set_state(key, None)
    assert await storage.get_state(key) is None

    await storage.set_data(key, {})
    assert await storage.get_data(key) == {}

    await storage.close()
    assert fake_client.closed is True
