from typing import TYPE_CHECKING, Any, Union, cast

from pydantic import Field

from aiosplus.types.base import SoroushObject
from aiosplus.types.chat import Chat, Location
from aiosplus.types.keyboards import (
    ForceReply,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiosplus.types.media import (
    Animation,
    Audio,
    Contact,
    Document,
    PhotoSize,
    Video,
    VideoNote,
    Voice,
)
from aiosplus.types.message_entity import MessageEntity
from aiosplus.types.sticker import Sticker
from aiosplus.types.user import User

if TYPE_CHECKING:
    from aiosplus.types.input_file import InputFile


class MessageId(SoroushObject):
    """This object represents a unique message identifier."""

    message_id: int


class Message(SoroushObject):
    """This object represents a Soroush Plus message."""

    message_id: int
    from_user: User | None = Field(default=None, alias="from")
    date: int
    chat: Chat
    forward_from: User | None = None
    forward_from_chat: Chat | None = None
    forward_from_message_id: int | None = None
    forward_signature: str | None = None
    forward_sender_name: str | None = None
    forward_date: int | None = None
    reply_to_message: Union["Message", None] = None
    via_bot: User | None = None
    edit_date: int | None = None
    has_protected_content: bool | None = None
    media_group_id: str | None = None
    text: str | None = None
    entities: list[MessageEntity] | None = None
    animation: Animation | None = None
    audio: Audio | None = None
    document: Document | None = None
    photo: list[PhotoSize] | None = None
    sticker: Sticker | None = None
    video: Video | None = None
    video_note: VideoNote | None = None
    voice: Voice | None = None
    caption: str | None = None
    caption_entities: list[MessageEntity] | None = None
    contact: Contact | None = None
    location: Location | None = None
    new_chat_title: str | None = None
    new_chat_photo: list[PhotoSize] | None = None
    pinned_message: Any | None = None
    reply_markup: InlineKeyboardMarkup | None = None

    @property
    def content_type(self) -> str:
        """Helper to determine the primary content type of the message."""
        if self.text:
            return "text"
        if self.photo:
            return "photo"
        if self.audio:
            return "audio"
        if self.document:
            return "document"
        if self.video:
            return "video"
        if self.voice:
            return "voice"
        if self.video_note:
            return "video_note"
        if self.animation:
            return "animation"
        if self.sticker:
            return "sticker"
        if self.contact:
            return "contact"
        if self.location:
            return "location"
        if self.new_chat_title:
            return "new_chat_title"
        if self.new_chat_photo:
            return "new_chat_photo"
        return "unknown"

    async def answer(
        self,
        text: str,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> "Message":
        """Convenience method to send a reply to the same chat."""
        if self._bot is None:
            raise RuntimeError("Bot instance is not bound to this Message object.")
        res = await self._bot.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
        )
        return cast("Message", res)

    async def reply(
        self,
        text: str,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
        allow_sending_without_reply: bool | None = None,
    ) -> "Message":
        """Convenience method to reply directly to this message."""
        if self._bot is None:
            raise RuntimeError("Bot instance is not bound to this Message object.")
        res = await self._bot.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_to_message_id=self.message_id,
            allow_sending_without_reply=allow_sending_without_reply,
            reply_markup=reply_markup,
        )
        return cast("Message", res)

    async def answer_photo(
        self,
        photo: Union[str, "InputFile"],
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> "Message":
        """Convenience method to send a photo to the same chat."""
        if self._bot is None:
            raise RuntimeError("Bot instance is not bound to this Message object.")
        res = await self._bot.send_photo(
            chat_id=self.chat.id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup,
        )
        return cast("Message", res)

    async def answer_document(
        self,
        document: Union[str, "InputFile"],
        caption: str | None = None,
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> "Message":
        """Convenience method to send a document to the same chat."""
        if self._bot is None:
            raise RuntimeError("Bot instance is not bound to this Message object.")
        res = await self._bot.send_document(
            chat_id=self.chat.id,
            document=document,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            reply_markup=reply_markup,
        )
        return cast("Message", res)

    async def delete(self) -> bool:
        """Convenience method to delete this message."""
        if self._bot is None:
            raise RuntimeError("Bot instance is not bound to this Message object.")
        res = await self._bot.delete_message(chat_id=self.chat.id, message_id=self.message_id)
        return cast(bool, res)

    async def edit_text(
        self,
        text: str,
        parse_mode: str | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> "Message | bool":
        """Convenience method to edit this message's text."""
        if self._bot is None:
            raise RuntimeError("Bot instance is not bound to this Message object.")
        res = await self._bot.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.message_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            reply_markup=reply_markup,
        )
        return cast("Message | bool", res)

    async def edit_reply_markup(
        self,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> "Message | bool":
        """Convenience method to edit this message's reply markup."""
        if self._bot is None:
            raise RuntimeError("Bot instance is not bound to this Message object.")
        res = await self._bot.edit_message_reply_markup(
            chat_id=self.chat.id,
            message_id=self.message_id,
            reply_markup=reply_markup,
        )
        return cast("Message | bool", res)

    async def pin(self) -> bool:
        """Convenience method to pin this message."""
        if self._bot is None:
            raise RuntimeError("Bot instance is not bound to this Message object.")
        res = await self._bot.pin_chat_message(chat_id=self.chat.id, message_id=self.message_id)
        return cast(bool, res)
