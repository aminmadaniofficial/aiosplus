from __future__ import annotations

import re
from collections.abc import Callable, Sequence
from re import Pattern
from typing import Any


class MagicFilter:
    """Magic Filter object allowing expressive attribute path matching (e.g. F.text == 'hi')."""

    def __init__(
        self, path: Sequence[str] = (), operation: Callable[[Any], bool] | None = None
    ) -> None:
        self._path = tuple(path)
        self._operation = operation

    def __getattr__(self, name: str) -> MagicFilter:
        if name.startswith("_"):
            raise AttributeError(name)
        return MagicFilter(path=(*self._path, name), operation=self._operation)

    def _resolve(self, obj: Any) -> Any:
        current = obj
        for attr in self._path:
            if current is None:
                return None
            if isinstance(current, dict):
                current = current.get(attr)
            elif hasattr(current, attr):
                current = getattr(current, attr)
            else:
                return None
        return current

    def resolve(self, obj: Any) -> bool:
        """Evaluate the filter against the object."""
        if not self._path and self._operation is not None:
            return bool(self._operation(obj))

        val = self._resolve(obj)
        if self._operation is not None:
            try:
                return bool(self._operation(val))
            except Exception:
                return False
        return bool(val)

    async def __call__(self, event: Any, **kwargs: Any) -> bool | dict[str, Any]:
        del kwargs
        return self.resolve(event)

    def __eq__(self, other: Any) -> MagicFilter:  # type: ignore[override]
        return MagicFilter(
            path=self._path,
            operation=lambda v: v == other,
        )

    def __ne__(self, other: Any) -> MagicFilter:  # type: ignore[override]
        return MagicFilter(
            path=self._path,
            operation=lambda v: v != other,
        )

    def __invert__(self) -> MagicFilter:
        return MagicFilter(
            path=(),
            operation=lambda obj: not self.resolve(obj),
        )

    def __and__(self, other: MagicFilter) -> MagicFilter:
        return MagicFilter(
            path=(),
            operation=lambda obj: self.resolve(obj) and other.resolve(obj),
        )

    def __or__(self, other: MagicFilter) -> MagicFilter:
        return MagicFilter(
            path=(),
            operation=lambda obj: self.resolve(obj) or other.resolve(obj),
        )

    def startswith(self, prefix: str) -> MagicFilter:
        return MagicFilter(
            path=self._path,
            operation=lambda v: isinstance(v, str) and v.startswith(prefix),
        )

    def endswith(self, suffix: str) -> MagicFilter:
        return MagicFilter(
            path=self._path,
            operation=lambda v: isinstance(v, str) and v.endswith(suffix),
        )

    def contains(self, substring: str) -> MagicFilter:
        return MagicFilter(
            path=self._path,
            operation=lambda v: v is not None and substring in v,
        )

    def in_(self, container: Sequence[Any]) -> MagicFilter:
        return MagicFilter(
            path=self._path,
            operation=lambda v: v in container,
        )

    def regexp(self, pattern: str | Pattern[str]) -> MagicFilter:
        compiled = re.compile(pattern) if isinstance(pattern, str) else pattern
        return MagicFilter(
            path=self._path,
            operation=lambda v: isinstance(v, str) and bool(compiled.search(v)),
        )

    def func(self, predicate: Callable[[Any], bool]) -> MagicFilter:
        return MagicFilter(
            path=self._path,
            operation=lambda v: bool(predicate(v)),
        )


F = MagicFilter()
