from __future__ import annotations

from typing import TYPE_CHECKING, Any

from aiosplus.types.update import Update

if TYPE_CHECKING:
    from aiosplus.bot.bot import Bot
    from aiosplus.dispatcher.dispatcher import Dispatcher


class SimpleWebhookHandler:
    """Helper to process webhook JSON payloads."""

    def __init__(self, dispatcher: Dispatcher, bot: Bot) -> None:
        self.dispatcher = dispatcher
        self.bot = bot

    async def feed_raw_update(self, raw_data: dict[str, Any], **kwargs: Any) -> bool:
        """Parse raw JSON update dict and pass through Dispatcher."""
        update = Update.model_validate(raw_data).as_bot(self.bot)
        if update.event:
            update.event.as_bot(self.bot)
        return await self.dispatcher.feed_update(self.bot, update, **kwargs)
