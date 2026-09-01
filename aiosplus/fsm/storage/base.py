from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from aiosplus.fsm.state import State


@dataclass(frozen=True)
class StorageKey:
    """Unique key identifying state and data in storage."""

    bot_id: int
    chat_id: int
    user_id: int
    destiny: str = "default"


class BaseStorage(ABC):
    """Abstract base class for all FSM storage backends."""

    @abstractmethod
    async def set_state(self, key: StorageKey, state: str | State | None = None) -> None:
        """Set state for key."""
        pass

    @abstractmethod
    async def get_state(self, key: StorageKey) -> str | None:
        """Get current state for key."""
        pass

    @abstractmethod
    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        """Set user data for key."""
        pass

    @abstractmethod
    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        """Get user data for key."""
        pass

    @abstractmethod
    async def update_data(
        self, key: StorageKey, data: dict[str, Any] | None = None, **kwargs: Any
    ) -> dict[str, Any]:
        """Update user data for key with new dictionary or kwargs."""
        pass

    @abstractmethod
    async def close(self) -> None:
        """Close storage connections if applicable."""
        pass
