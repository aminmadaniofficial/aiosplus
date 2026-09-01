from aiosplus.types.base import SoroushObject


class BotCommand(SoroushObject):
    """This object represents a bot command."""

    command: str
    description: str


class BotCommandScope(SoroushObject):
    """Base class for bot command scopes."""

    type: str


class BotCommandScopeDefault(BotCommandScope):
    """Represents the default scope of bot commands."""

    type: str = "default"


class BotCommandScopeAllPrivateChats(BotCommandScope):
    """Represents the scope of bot commands covering all private chats."""

    type: str = "all_private_chats"


class BotCommandScopeChat(BotCommandScope):
    """Represents the scope of bot commands covering a specific chat."""

    type: str = "chat"
    chat_id: int | str
