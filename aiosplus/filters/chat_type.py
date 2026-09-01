from collections.abc import Sequence
from typing import Any

from aiosplus.enums import ChatType
from aiosplus.filters.base import BaseFilter
from aiosplus.types.message import Message


class ChatTypeFilter(BaseFilter):
    """Filter to match chat types (private, group, supergroup, channel)."""

    def __init__(self, chat_types: ChatType | str | Sequence[ChatType | str]) -> None:
        if isinstance(chat_types, (str, ChatType)):
            self.chat_types = {str(chat_types)}
        else:
            self.chat_types = {str(ct) for ct in chat_types}

    async def __call__(self, event: Any, **kwargs: Any) -> bool | dict[str, Any]:
        del kwargs
        if isinstance(event, Message) and event.chat:
            return str(event.chat.type) in self.chat_types
        return False
