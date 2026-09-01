from abc import ABC, abstractmethod
from typing import Any


class BaseFilter(ABC):
    """Abstract base class for all filters."""

    @abstractmethod
    async def __call__(self, event: Any, **kwargs: Any) -> bool | dict[str, Any]:
        """Evaluate the filter against the given event and context data."""
        pass
