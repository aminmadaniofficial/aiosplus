from __future__ import annotations

import json
from typing import Any

from aiosplus.fsm.state import State
from aiosplus.fsm.storage.base import BaseStorage, StorageKey


class RedisStorage(BaseStorage):
    """Redis-backed storage for FSM states and user data."""

    def __init__(
        self,
        redis: Any,
        key_prefix: str = "fsm",
        state_ttl: int | None = None,
        data_ttl: int | None = None,
    ) -> None:
        self.redis = redis
        self.key_prefix = key_prefix
        self.state_ttl = state_ttl
        self.data_ttl = data_ttl

    @classmethod
    def from_url(
        cls,
        url: str,
        key_prefix: str = "fsm",
        state_ttl: int | None = None,
        data_ttl: int | None = None,
        **connection_kwargs: Any,
    ) -> RedisStorage:
        """Create RedisStorage from connection string URL."""
        try:
            import redis.asyncio as aioredis
        except ImportError as exc:
            raise ImportError(
                "redis package is required for RedisStorage. Install it via 'pip install redis' or 'pip install aiosplus[redis]'"
            ) from exc
        client = aioredis.from_url(url, **connection_kwargs)
        return cls(redis=client, key_prefix=key_prefix, state_ttl=state_ttl, data_ttl=data_ttl)

    def _state_key(self, key: StorageKey) -> str:
        return f"{self.key_prefix}:{key.bot_id}:{key.chat_id}:{key.user_id}:state"

    def _data_key(self, key: StorageKey) -> str:
        return f"{self.key_prefix}:{key.bot_id}:{key.chat_id}:{key.user_id}:data"

    async def set_state(self, key: StorageKey, state: str | State | None = None) -> None:
        redis_key = self._state_key(key)
        str_state = state.state if isinstance(state, State) else state
        if str_state is None:
            await self.redis.delete(redis_key)
        else:
            await self.redis.set(redis_key, str_state, ex=self.state_ttl)

    async def get_state(self, key: StorageKey) -> str | None:
        redis_key = self._state_key(key)
        raw = await self.redis.get(redis_key)
        if raw is None:
            return None
        return raw.decode("utf-8") if isinstance(raw, bytes) else str(raw)

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        redis_key = self._data_key(key)
        if not data:
            await self.redis.delete(redis_key)
        else:
            payload = json.dumps(data)
            await self.redis.set(redis_key, payload, ex=self.data_ttl)

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        redis_key = self._data_key(key)
        raw = await self.redis.get(redis_key)
        if raw is None:
            return {}
        text = raw.decode("utf-8") if isinstance(raw, bytes) else str(raw)
        return json.loads(text)  # type: ignore[no-any-return]

    async def update_data(
        self, key: StorageKey, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        current = await self.get_data(key)
        if data:
            current.update(data)
        if kwargs:
            current.update(kwargs)
        await self.set_data(key, current)
        return current

    async def close(self) -> None:
        if hasattr(self.redis, "aclose"):
            await self.redis.aclose()
        elif hasattr(self.redis, "close"):
            res = self.redis.close()
            if hasattr(res, "__await__"):
                await res
