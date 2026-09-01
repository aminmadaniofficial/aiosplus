from __future__ import annotations

import inspect
from collections.abc import Awaitable, Callable, Sequence
from typing import Any

from aiosplus.filters.base import BaseFilter
from aiosplus.middlewares.base import BaseMiddleware, HandlerType

CallbackType = Callable[..., Awaitable[Any]]


class EventHandler:
    """Wraps an asynchronous callback function and its associated filters."""

    def __init__(
        self, callback: CallbackType, filters: Sequence[BaseFilter | Callable[..., Any]] = ()
    ) -> None:
        self.callback = callback
        self.filters = list(filters)
        self.spec = inspect.getfullargspec(callback)

    async def check_filters(self, event: Any, data: dict[str, Any]) -> tuple[bool, dict[str, Any]]:
        """Check all filters against the event. Returns (is_matched, extra_data)."""
        extra_data: dict[str, Any] = {}
        for f in self.filters:
            if isinstance(f, BaseFilter) or callable(f):
                res = f(event, **data, **extra_data)
                if inspect.isawaitable(res):
                    res = await res
                if not res:
                    return False, {}
                if isinstance(res, dict):
                    extra_data.update(res)
        return True, extra_data

    async def call(self, event: Any, data: dict[str, Any]) -> Any:
        """Call the underlying handler with matching keyword arguments or positional event."""
        kwargs: dict[str, Any] = {}
        # Pass kwargs that exist in callback signature
        for k, v in data.items():
            if self.spec.varkw is not None or k in self.spec.args or k in self.spec.kwonlyargs:
                kwargs[k] = v

        if self.spec.args and len(self.spec.args) > 0 and self.spec.args[0] not in kwargs:
            return await self.callback(event, **kwargs)
        return await self.callback(**kwargs) if kwargs else await self.callback(event)


class EventObserver:
    """Observer managing handlers and middlewares for a specific event type."""

    def __init__(self, event_name: str) -> None:
        self.event_name = event_name
        self.handlers: list[EventHandler] = []
        self.middlewares: list[BaseMiddleware] = []
        self.outer_middlewares: list[BaseMiddleware] = []

    def register(
        self,
        callback: CallbackType,
        *filters: BaseFilter | Callable[..., Any],
    ) -> CallbackType:
        """Register a handler callback with filters."""
        self.handlers.append(EventHandler(callback=callback, filters=filters))
        return callback

    def __call__(
        self,
        *filters: BaseFilter | Callable[..., Any],
    ) -> Callable[[CallbackType], CallbackType]:
        """Decorator for registering an event handler."""

        def decorator(callback: CallbackType) -> CallbackType:
            return self.register(callback, *filters)

        return decorator

    def middleware(self, middleware: BaseMiddleware) -> BaseMiddleware:
        """Register an inner middleware."""
        self.middlewares.append(middleware)
        return middleware

    def outer_middleware(self, middleware: BaseMiddleware) -> BaseMiddleware:
        """Register an outer middleware."""
        self.outer_middlewares.append(middleware)
        return middleware

    def _wrap_middleware(
        self, middlewares: list[BaseMiddleware], target: HandlerType
    ) -> HandlerType:
        handler = target
        for m in reversed(middlewares):
            prev_handler = handler

            def make_step(mw: BaseMiddleware, next_h: HandlerType) -> HandlerType:
                async def step(ev: Any, dt: dict[str, Any]) -> Any:
                    return await mw(next_h, ev, dt)

                return step

            handler = make_step(m, prev_handler)
        return handler

    async def trigger(self, event: Any, **data: Any) -> bool:
        """Trigger handlers for this event."""

        # Execute outer middlewares
        async def run_handlers(ev: Any, dt: dict[str, Any]) -> bool:
            for handler in self.handlers:
                matched, extra_data = await handler.check_filters(ev, dt)
                if matched:
                    call_data = {**dt, **extra_data}

                    def make_final_handler(h: EventHandler) -> HandlerType:
                        async def final_handler(h_ev: Any, h_dt: dict[str, Any]) -> Any:
                            return await h.call(h_ev, h_dt)

                        return final_handler

                    pipeline = self._wrap_middleware(self.middlewares, make_final_handler(handler))
                    await pipeline(ev, call_data)
                    return True
            return False

        outer_pipeline = self._wrap_middleware(self.outer_middlewares, run_handlers)
        return bool(await outer_pipeline(event, data))
