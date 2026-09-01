from __future__ import annotations

import contextvars
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from aiosplus.bot.bot import Bot

_current_bot: contextvars.ContextVar[Bot] = contextvars.ContextVar("current_bot")


def get_current_bot() -> Bot | None:
    """Retrieve the currently active Bot instance from contextvars."""
    try:
        return _current_bot.get()
    except LookupError:
        return None


def set_current_bot(bot: Bot) -> contextvars.Token[Bot]:
    """Set the active Bot instance in contextvars."""
    return _current_bot.set(bot)


def reset_current_bot(token: contextvars.Token[Bot]) -> None:
    """Reset the active Bot instance in contextvars."""
    _current_bot.reset(token)
