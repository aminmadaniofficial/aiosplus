from __future__ import annotations

from typing import Any

from aiosplus.dispatcher.event import EventObserver


class Router:
    """Modular event router for structuring bot handlers into blueprints."""

    def __init__(self, name: str | None = None) -> None:
        self.name = name or self.__class__.__name__
        self.sub_routers: list[Router] = []
        self.parent_router: Router | None = None

        # Observers for different event types
        self.message = EventObserver("message")
        self.edited_message = EventObserver("edited_message")
        self.callback_query = EventObserver("callback_query")
        self.update = EventObserver("update")

        self.observers: dict[str, EventObserver] = {
            "message": self.message,
            "edited_message": self.edited_message,
            "callback_query": self.callback_query,
            "update": self.update,
        }

    def include_router(self, router: Router) -> Router:
        """Attach a sub-router to this router."""
        if router is self:
            raise ValueError("Cannot include router into itself.")
        if router in self.sub_routers:
            raise ValueError(f"Router {router} is already included.")
        router.parent_router = self
        self.sub_routers.append(router)
        return router

    def include_routers(self, *routers: Router) -> None:
        """Attach multiple sub-routers."""
        for r in routers:
            self.include_router(r)

    async def propagate_event(self, event_type: str, event: Any, **data: Any) -> bool:
        """Pass event through observers and sub-routers."""
        observer = self.observers.get(event_type)
        if observer is not None:
            handled = await observer.trigger(event, **data)
            if handled:
                return True

        for sub_router in self.sub_routers:
            handled = await sub_router.propagate_event(event_type, event, **data)
            if handled:
                return True

        return False
