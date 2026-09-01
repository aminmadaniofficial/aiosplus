from aiosplus.types.base import SoroushObject
from aiosplus.types.user import User


class MessageEntity(SoroushObject):
    """This object represents one special entity in a text message."""

    type: str
    offset: int
    length: int
    url: str | None = None
    user: User | None = None
    language: str | None = None
