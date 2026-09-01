from pydantic import Field

from aiosplus.types.base import SoroushObject


class InlineKeyboardButton(SoroushObject):
    """This object represents one button of an inline keyboard."""

    text: str
    url: str | None = None
    callback_data: str | None = None


class InlineKeyboardMarkup(SoroushObject):
    """This object represents an inline keyboard that appears right next to the message it belongs to."""

    inline_keyboard: list[list[InlineKeyboardButton]] = Field(default_factory=list)


class KeyboardButton(SoroushObject):
    """This object represents one button of the reply keyboard."""

    text: str
    request_contact: bool | None = None
    request_location: bool | None = None


class ReplyKeyboardMarkup(SoroushObject):
    """This object represents a custom keyboard with reply options."""

    keyboard: list[list[KeyboardButton]] = Field(default_factory=list)
    resize_keyboard: bool | None = None
    one_time_keyboard: bool | None = None
    input_field_placeholder: str | None = None


class ReplyKeyboardRemove(SoroushObject):
    """Requests clients to remove the custom keyboard and display default keyboard."""

    remove_keyboard: bool = True
    selective: bool | None = None


class ForceReply(SoroushObject):
    """Displays a reply interface to the user as if they chose to reply to the bot's message."""

    force_reply: bool = True
    input_field_placeholder: str | None = None
    selective: bool | None = None
