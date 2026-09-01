from aiosplus.types.base import SoroushObject
from aiosplus.types.callback_query import CallbackQuery
from aiosplus.types.message import Message


class Update(SoroushObject):
    """This object represents an incoming update."""

    update_id: int
    message: Message | None = None
    edited_message: Message | None = None
    callback_query: CallbackQuery | None = None

    @property
    def event(self) -> Message | CallbackQuery | None:
        """Return the active event contained within this update."""
        if self.message is not None:
            return self.message
        if self.edited_message is not None:
            return self.edited_message
        if self.callback_query is not None:
            return self.callback_query
        return None

    @property
    def event_type(self) -> str:
        """Return the name of the active event."""
        if self.message is not None:
            return "message"
        if self.edited_message is not None:
            return "edited_message"
        if self.callback_query is not None:
            return "callback_query"
        return "unknown"
