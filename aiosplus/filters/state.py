from __future__ import annotations

from typing import Any

from aiosplus.filters.base import BaseFilter
from aiosplus.fsm.context import FSMContext
from aiosplus.fsm.state import State

ANY_STATE = "*"


class StateFilter(BaseFilter):
    """Filter to match current FSM state."""

    def __init__(self, *states: State | str | None) -> None:
        self.states: set[str | None] = set()
        self.any_state = False

        for s in states:
            if s == ANY_STATE:
                self.any_state = True
            elif isinstance(s, State):
                self.states.add(s.state)
            elif isinstance(s, str):
                self.states.add(s)
            elif s is None:
                self.states.add(None)

    async def __call__(self, event: Any, **kwargs: Any) -> bool | dict[str, Any]:
        del event
        if self.any_state:
            return True

        state_ctx: FSMContext | None = kwargs.get("state")
        raw_state: str | None = kwargs.get("raw_state")

        current_state: str | None = raw_state
        if current_state is None and state_ctx is not None:
            current_state = await state_ctx.get_state()

        return current_state in self.states
