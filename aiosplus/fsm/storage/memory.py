from __future__ import annotations

import copy
from typing import Any

from aiosplus.fsm.state import State
from aiosplus.fsm.storage.base import BaseStorage, StorageKey


class MemoryStorage(BaseStorage):
    """Thread-safe in-memory storage for states and data."""

    def __init__(self) -> None:
        self._states: dict[StorageKey, str | None] = {}
        self._data: dict[StorageKey, dict[str, Any]] = {}

    async def set_state(self, key: StorageKey, state: str | State | None = None) -> None:
        str_state = state.state if isinstance(state, State) else state
        if str_state is None:
            self._states.pop(key, None)
        else:
            self._states[key] = str_state

    async def get_state(self, key: StorageKey) -> str | None:
        return self._states.get(key)

    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        if not data:
            self._data.pop(key, None)
        else:
            self._data[key] = copy.deepcopy(data)

    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        return copy.deepcopy(self._data.get(key, {}))

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
        self._states.clear()
        self._data.clear()
