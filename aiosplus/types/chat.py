from typing import Any

from aiosplus.types.base import SoroushObject


class ChatPhoto(SoroushObject):
    """This object represents a chat photo."""

    small_file_id: str
    small_file_unique_id: str
    big_file_id: str
    big_file_unique_id: str


class ChatPermissions(SoroushObject):
    """Describes actions that a non-administrator user is allowed to take in a chat."""

    can_send_messages: bool | None = None
    can_send_media_messages: bool | None = None
    can_send_polls: bool | None = None
    can_send_other_messages: bool | None = None
    can_add_web_page_previews: bool | None = None
    can_change_info: bool | None = None
    can_invite_users: bool | None = None
    can_pin_messages: bool | None = None


class Location(SoroushObject):
    """This object represents a point on the map."""

    latitude: float
    longitude: float
    horizontal_accuracy: float | None = None


class ChatLocation(SoroushObject):
    """Represents a location to which a chat is connected."""

    location: Location
    address: str


class Chat(SoroushObject):
    """This object represents a chat."""

    id: int
    type: str
    title: str | None = None
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    photo: ChatPhoto | None = None
    bio: str | None = None
    description: str | None = None
    invite_link: str | None = None
    pinned_message: Any | None = None
    permissions: ChatPermissions | None = None
    slow_mode_delay: int | None = None
    message_auto_delete_time: int | None = None
    has_protected_content: bool | None = None
    sticker_set_name: str | None = None
    can_set_sticker_set: bool | None = None
    linked_chat_id: int | None = None
    location: ChatLocation | None = None
    all_members_are_administrators: bool | None = None

    @property
    def full_name(self) -> str:
        """Full name for private chat or title for group/channel."""
        if self.title:
            return self.title
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name or ""
