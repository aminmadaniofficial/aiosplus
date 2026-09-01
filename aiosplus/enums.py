from enum import Enum


class StrEnum(str, Enum):
    """Base string enum that compares equal to its string value."""

    def __str__(self) -> str:
        return str(self.value)


class ParseMode(StrEnum):
    """Supported parse modes for message formatting."""

    MARKDOWN_V2 = "MarkdownV2"
    HTML = "HTML"
    MARKDOWN = "Markdown"


class ChatType(StrEnum):
    """Types of chats in Soroush Plus."""

    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"


class MessageEntityType(StrEnum):
    """Types of message entities."""

    MENTION = "mention"
    HASHTAG = "hashtag"
    CASHTAG = "cashtag"
    BOT_COMMAND = "bot_command"
    URL = "url"
    EMAIL = "email"
    PHONE_NUMBER = "phone_number"
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    STRIKETHROUGH = "strikethrough"
    SPOILER = "spoiler"
    BLOCKQUOTE = "blockquote"
    EXPANDABLE_BLOCKQUOTE = "expandable_blockquote"
    CODE = "code"
    PRE = "pre"
    TEXT_LINK = "text_link"
    TEXT_MENTION = "text_mention"
    CUSTOM_EMOJI = "custom_emoji"
    DATE_TIME = "date_time"


class ChatAction(StrEnum):
    """Types of chat actions for sendChatAction."""

    TYPING = "typing"
    UPLOAD_PHOTO = "upload_photo"
    RECORD_VIDEO = "record_video"
    UPLOAD_VIDEO = "upload_video"
    RECORD_VOICE = "record_voice"
    UPLOAD_VOICE = "upload_voice"
    UPLOAD_DOCUMENT = "upload_document"
    CHOOSE_STICKER = "choose_sticker"
    FIND_LOCATION = "find_location"
    RECORD_VIDEO_NOTE = "record_video_note"
    UPLOAD_VIDEO_NOTE = "upload_video_note"


class BotCommandScopeType(StrEnum):
    """Types of bot command scopes."""

    DEFAULT = "default"
    ALL_PRIVATE_CHATS = "all_private_chats"
    CHAT = "chat"


class MaskPoint(StrEnum):
    """Part of the face on which the mask should be placed."""

    FOREHEAD = "forehead"
    EYES = "eyes"
    MOUTH = "mouth"
    CHIN = "chin"
