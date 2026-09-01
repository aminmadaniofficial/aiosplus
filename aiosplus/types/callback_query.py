from typing import cast

from pydantic import Field

from aiosplus.types.base import SoroushObject
from aiosplus.types.message import Message
from aiosplus.types.user import User


class CallbackQuery(SoroushObject):
    """This object represents an incoming callback query from a callback button in an inline keyboard."""

    id: str
    from_user: User = Field(alias="from")
    message: Message | None = None
    data: str | None = None

    async def answer(
        self,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
    ) -> bool:
        """Convenience method to answer this callback query."""
        if self._bot is None:
            raise RuntimeError("Bot instance is not bound to this CallbackQuery object.")
        res = await self._bot.answer_callback_query(
            callback_query_id=self.id,
            text=text,
            show_alert=show_alert,
            url=url,
            cache_time=cache_time,
        )
        return cast(bool, res)
