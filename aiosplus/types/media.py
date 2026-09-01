from aiosplus.types.base import SoroushObject
from aiosplus.types.photo_size import PhotoSize


class Animation(SoroushObject):
    """This object represents an animation file (GIF or video without sound)."""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: PhotoSize | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None


class Audio(SoroushObject):
    """This object represents an audio file to be treated as music."""

    file_id: str
    file_unique_id: str
    duration: int
    performer: str | None = None
    title: str | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None
    thumb: PhotoSize | None = None


class Document(SoroushObject):
    """This object represents a general file (as opposed to photos or audio)."""

    file_id: str
    file_unique_id: str
    thumb: PhotoSize | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None


class Video(SoroushObject):
    """This object represents a video file."""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    duration: int
    thumb: PhotoSize | None = None
    file_name: str | None = None
    mime_type: str | None = None
    file_size: int | None = None


class VideoNote(SoroushObject):
    """This object represents a video message (round video note)."""

    file_id: str
    file_unique_id: str
    length: int
    duration: int
    thumb: PhotoSize | None = None
    file_size: int | None = None


class Voice(SoroushObject):
    """This object represents a voice note."""

    file_id: str
    file_unique_id: str
    duration: int
    mime_type: str | None = None
    file_size: int | None = None


class Contact(SoroushObject):
    """This object represents a phone contact."""

    phone_number: str
    first_name: str
    last_name: str | None = None
    user_id: int | None = None
    vcard: str | None = None


class UserProfilePhotos(SoroushObject):
    """This object represent a user's profile pictures."""

    total_count: int
    photos: list[list[PhotoSize]]


class File(SoroushObject):
    """This object represents a file ready to be downloaded."""

    file_id: str
    file_unique_id: str
    file_size: int | None = None
    file_path: str | None = None
