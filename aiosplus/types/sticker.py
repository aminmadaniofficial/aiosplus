from aiosplus.types.base import SoroushObject
from aiosplus.types.photo_size import PhotoSize


class MaskPosition(SoroushObject):
    """This object describes the position on faces where a mask should be placed."""

    point: str
    x_shift: float
    y_shift: float
    scale: float


class Sticker(SoroushObject):
    """This object represents a sticker."""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    is_animated: bool
    is_video: bool
    thumb: PhotoSize | None = None
    emoji: str | None = None
    set_name: str | None = None
    mask_position: MaskPosition | None = None
    file_size: int | None = None


class StickerSet(SoroushObject):
    """This object represents a sticker set."""

    name: str
    title: str
    stickers: list[Sticker]
    thumb: PhotoSize | None = None
