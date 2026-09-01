from abc import ABC, abstractmethod
from collections.abc import Awaitable, Callable
from typing import Any

HandlerType = Callable[[Any, dict[str, Any]], Awaitable[Any]]


class BaseMiddleware(ABC):
    """Abstract base class for all middlewares."""

    @abstractmethod
    async def __call__(
        self,
        handler: HandlerType,
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        """Execute middleware logic before/after the handler."""
        pass
