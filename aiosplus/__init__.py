"""aiosplus - Modern, asynchronous Python framework for Soroush Plus Bot API."""

from aiosplus.client.session import AioSplusSession
from aiosplus.enums import (
    BotCommandScopeType,
    ChatAction,
    ChatType,
    MaskPoint,
    MessageEntityType,
    ParseMode,
)
from aiosplus.exceptions import (
    NetworkError,
    RestartingUpdateError,
    SoroushAPIError,
    SoroushBadRequest,
    SoroushConflictError,
    SoroushException,
    SoroushFloodError,
    SoroushForbidden,
    SoroushNotFound,
    SoroushServerError,
    SoroushUnauthorized,
)

__version__ = "0.1.0"
__author__ = "Amin Madani"
__all__ = [
    "__version__",
    "AioSplusSession",
    "ParseMode",
    "ChatType",
    "MessageEntityType",
    "ChatAction",
    "BotCommandScopeType",
    "MaskPoint",
    "SoroushException",
    "NetworkError",
    "SoroushAPIError",
    "SoroushBadRequest",
    "SoroushUnauthorized",
    "SoroushForbidden",
    "SoroushNotFound",
    "SoroushConflictError",
    "SoroushFloodError",
    "SoroushServerError",
    "RestartingUpdateError",
]
