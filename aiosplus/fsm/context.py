from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aiosplus.fsm.state import State
    from aiosplus.fsm.storage.base import BaseStorage, StorageKey


class FSMContext:
    """Context manager for inspecting and mutating FSM state and data for a specific user and chat."""

    def __init__(self, storage: BaseStorage, key: StorageKey) -> None:
        self.storage = storage
        self.key = key

    async def set_state(self, state: str | State | None = None) -> None:
        """Set current state."""
        await self.storage.set_state(self.key, state)

    async def get_state(self) -> str | None:
        """Get current state."""
        return await self.storage.get_state(self.key)

    async def set_data(self, data: dict[str, Any]) -> None:
        """Overwrite context data."""
        await self.storage.set_data(self.key, data)

    async def get_data(self) -> dict[str, Any]:
        """Get context data."""
        return await self.storage.get_data(self.key)

    async def update_data(
        self, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        """Update context data."""
        return await self.storage.update_data(self.key, data=data, **kwargs)

    async def clear(self) -> None:
        """Clear both state and context data."""
        await self.set_state(state=None)
        await self.set_data(data={})
