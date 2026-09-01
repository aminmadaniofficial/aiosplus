from __future__ import annotations

import logging
import time
from typing import Any

from aiosplus.middlewares.base import BaseMiddleware, HandlerType

logger = logging.getLogger("aiosplus.middleware.logging")


class LoggingMiddleware(BaseMiddleware):
    """Middleware that logs the arrival and duration of processed events."""

    def __init__(self, log_level: int = logging.INFO) -> None:
        self.log_level = log_level

    async def __call__(
        self,
        handler: HandlerType,
        event: Any,
        data: dict[str, Any],
    ) -> Any:
        start_time = time.perf_counter()
        event_repr = repr(event)
        logger.log(self.log_level, f"Handling event: {event_repr[:120]}")

        try:
            result = await handler(event, data)
            elapsed = (time.perf_counter() - start_time) * 1000
            logger.log(self.log_level, f"Finished handling event in {elapsed:.2f}ms")
            return result
        except Exception as exc:
            elapsed = (time.perf_counter() - start_time) * 1000
            logger.error(f"Error handling event in {elapsed:.2f}ms: {exc}", exc_info=True)
            raise exc
