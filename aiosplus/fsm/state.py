from __future__ import annotations

from typing import Any


class State:
    """Represents a state in a finite state machine."""

    def __init__(self, state: str | None = None, group_name: str | None = None) -> None:
        self._state = state
        self._group_name = group_name

    @property
    def state(self) -> str | None:
        if self._state is not None and self._group_name is not None:
            return f"{self._group_name}:{self._state}"
        return self._state

    def __str__(self) -> str:
        return self.state or ""

    def __repr__(self) -> str:
        return f"<State '{self.state}'>"

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, State):
            return self.state == other.state
        if isinstance(other, str):
            return self.state == other
        return False

    def __hash__(self) -> int:
        return hash(self.state)


class StatesGroupMeta(type):
    """Metaclass that automatically names State attributes on a StatesGroup."""

    def __new__(mcs, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> type:
        cls = super().__new__(mcs, name, bases, namespace)
        for attr_name, value in namespace.items():
            if isinstance(value, State):
                value._state = attr_name
                value._group_name = name
        return cls


class StatesGroup(metaclass=StatesGroupMeta):
    """Base class for defining groups of states."""

    pass
