from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

from aiosplus.dispatcher.router import Router
from aiosplus.exceptions import SoroushConflictError
from aiosplus.types.update import Update

if TYPE_CHECKING:
    from aiosplus.bot.bot import Bot
    from aiosplus.fsm.context import FSMContext
    from aiosplus.fsm.storage.base import BaseStorage

logger = logging.getLogger("aiosplus.dispatcher")


class Dispatcher(Router):
    """Root event dispatcher."""

    def __init__(
        self,
        storage: BaseStorage | None = None,
        name: str = "Dispatcher",
    ) -> None:
        super().__init__(name=name)
        self.storage = storage

    def get_fsm_context(
        self,
        bot: Bot,
        chat_id: int | None = None,
        user_id: int | None = None,
    ) -> FSMContext | None:
        """Create or get FSMContext if storage is configured."""
        if self.storage is None:
            return None
        from aiosplus.fsm.context import FSMContext
        from aiosplus.fsm.storage.base import StorageKey

        actual_chat_id = chat_id or user_id or 0
        actual_user_id = user_id or chat_id or 0
        key = StorageKey(
            bot_id=id(bot),
            chat_id=actual_chat_id,
            user_id=actual_user_id,
        )
        return FSMContext(storage=self.storage, key=key)

    async def feed_update(self, bot: Bot, update: Update, **kwargs: Any) -> bool:
        """Feed an incoming update through the router pipeline."""
        from aiosplus.bot.context import set_current_bot

        set_current_bot(bot)
        update.as_bot(bot)
        event = update.event
        event_type = update.event_type

        # Inject context data
        data: dict[str, Any] = {
            "bot": bot,
            "raw_update": update,
            **kwargs,
        }

        # Extract chat and user ID for FSMContext injection
        chat_id: int | None = None
        user_id: int | None = None

        if update.message is not None:
            chat_id = update.message.chat.id
            if update.message.from_user:
                user_id = update.message.from_user.id
        elif update.edited_message is not None:
            chat_id = update.edited_message.chat.id
            if update.edited_message.from_user:
                user_id = update.edited_message.from_user.id
        elif update.callback_query is not None:
            if update.callback_query.message:
                chat_id = update.callback_query.message.chat.id
            user_id = update.callback_query.from_user.id

        if self.storage is not None and (chat_id is not None or user_id is not None):
            state_ctx = self.get_fsm_context(bot, chat_id=chat_id, user_id=user_id)
            data["state"] = state_ctx
            if state_ctx is not None:
                data["raw_state"] = await state_ctx.get_state()

        # Try to handle specific event
        if event is not None and event_type != "unknown":
            handled = await self.propagate_event(event_type, event, **data)
            if handled:
                return True

        # Fallback to general update observer
        return await self.propagate_event("update", update, **data)

    async def start_polling(
        self,
        bot: Bot,
        offset: int | None = None,
        limit: int = 100,
        timeout: int = 30,
        allowed_updates: list[str] | None = None,
        drop_pending_updates: bool = False,
        **kwargs: Any,
    ) -> None:
        """Start Long Polling update retrieval loop."""
        if drop_pending_updates:
            logger.info("Dropping pending updates...")
            await bot.delete_webhook(drop_pending_updates=True)

        current_offset = offset or 0
        logger.info("Starting polling for bot...")

        try:
            while True:
                try:
                    updates = await bot.get_updates(
                        offset=current_offset,
                        limit=limit,
                        timeout=timeout,
                        allowed_updates=allowed_updates,
                    )
                    for update in updates:
                        current_offset = update.update_id + 1
                        asyncio.create_task(self.feed_update(bot, update, **kwargs))
                except SoroushConflictError:
                    logger.warning("Polling conflict detected. Backing off 5 seconds...")
                    await asyncio.sleep(5)
                except asyncio.CancelledError:
                    logger.info("Polling loop cancelled.")
                    break
                except Exception as err:
                    logger.error(f"Error in polling loop: {err}", exc_info=True)
                    await asyncio.sleep(2)
        finally:
            logger.info("Shutting down polling...")
            await bot.close_session()
