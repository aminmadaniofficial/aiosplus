from aiosplus.types.base import SoroushObject
from aiosplus.types.input_file import InputFile
from aiosplus.types.message_entity import MessageEntity


class InputMedia(SoroushObject):
    """Base class for media to be sent in an album or edited."""

    type: str
    media: str | InputFile
    caption: str | None = None
    parse_mode: str | None = None
    caption_entities: list[MessageEntity] | None = None


class InputMediaPhoto(InputMedia):
    """Represents a photo to be sent in an album."""

    type: str = "photo"


class InputMediaVideo(InputMedia):
    """Represents a video to be sent in an album."""

    type: str = "video"
    width: int | None = None
    height: int | None = None
    duration: int | None = None
    supports_streaming: bool | None = None


class InputMediaAnimation(InputMedia):
    """Represents an animation file to be sent."""

    type: str = "animation"
    width: int | None = None
    height: int | None = None
    duration: int | None = None


class InputMediaAudio(InputMedia):
    """Represents an audio file to be sent in an album."""

    type: str = "audio"
    duration: int | None = None
    performer: str | None = None
    title: str | None = None


class InputMediaDocument(InputMedia):
    """Represents a general document to be sent in an album."""

    type: str = "document"
    disable_content_type_detection: bool | None = None
