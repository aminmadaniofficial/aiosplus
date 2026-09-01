from aiosplus.types.base import SoroushObject


class PhotoSize(SoroushObject):
    """This object represents one size of a photo or a file / sticker thumbnail."""

    file_id: str
    file_unique_id: str
    width: int
    height: int
    file_size: int | None = None
