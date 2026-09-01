from typing import Any, TypeVar

from pydantic import BaseModel, ConfigDict, PrivateAttr

TSoroushObject = TypeVar("TSoroushObject", bound="SoroushObject")


class SoroushObject(BaseModel):
    """Base model for all Soroush Plus API types."""

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        extra="allow",
    )

    _bot: Any = PrivateAttr(default=None)

    @property
    def bot(self) -> Any:
        """Return the bound Bot instance if set or active context bot."""
        if self._bot is not None:
            return self._bot
        from aiosplus.bot.context import get_current_bot

        return get_current_bot()

    def as_bot(self: TSoroushObject, bot: Any) -> TSoroushObject:
        """Bind this object to a specific Bot instance."""
        self._bot = bot
        return self


class MutableSoroushObject(SoroushObject):
    """SoroushObject with mutable configuration."""

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        validate_assignment=True,
        extra="allow",
    )
