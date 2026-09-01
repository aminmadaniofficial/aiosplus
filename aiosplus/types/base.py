from typing import Any

from pydantic import BaseModel, ConfigDict, PrivateAttr


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
        """Return the bound Bot instance if set."""
        return self._bot

    def as_bot(self, bot: Any) -> "SoroushObject":
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
