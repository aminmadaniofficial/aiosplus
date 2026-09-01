import re
from collections.abc import Sequence
from re import Pattern
from typing import Any

from aiosplus.filters.base import BaseFilter
from aiosplus.types.callback_query import CallbackQuery
from aiosplus.types.message import Message


class Text(BaseFilter):
    """Filter to match text in messages or data in callback queries."""

    def __init__(
        self,
        text: str | Sequence[str] | None = None,
        startswith: str | Sequence[str] | None = None,
        endswith: str | Sequence[str] | None = None,
        contains: str | Sequence[str] | None = None,
        regexp: str | Pattern[str] | None = None,
        ignore_case: bool = False,
    ) -> None:
        self.text = [text] if isinstance(text, str) else text
        self.startswith = [startswith] if isinstance(startswith, str) else startswith
        self.endswith = [endswith] if isinstance(endswith, str) else endswith
        self.contains = [contains] if isinstance(contains, str) else contains
        self.regexp = (
            re.compile(regexp, re.IGNORECASE if ignore_case else 0)
            if isinstance(regexp, str)
            else regexp
        )
        self.ignore_case = ignore_case

    async def __call__(self, event: Any, **_kwargs: Any) -> bool | dict[str, Any]:
        target_str: str | None = None
        if isinstance(event, Message):
            target_str = event.text or event.caption
        elif isinstance(event, CallbackQuery):
            target_str = event.data

        if target_str is None:
            return False

        check_str = target_str.lower() if self.ignore_case else target_str

        if self.text is not None:
            opts = [t.lower() if self.ignore_case else t for t in self.text]
            if check_str not in opts:
                return False

        if self.startswith is not None:
            opts = [s.lower() if self.ignore_case else s for s in self.startswith]
            if not any(check_str.startswith(s) for s in opts):
                return False

        if self.endswith is not None:
            opts = [e.lower() if self.ignore_case else e for e in self.endswith]
            if not any(check_str.endswith(e) for e in opts):
                return False

        if self.contains is not None:
            opts = [c.lower() if self.ignore_case else c for c in self.contains]
            if not any(c in check_str for c in opts):
                return False

        if self.regexp is not None:
            match = self.regexp.search(target_str)
            if not match:
                return False
            return {"match": match}

        return True
