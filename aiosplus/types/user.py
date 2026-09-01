from aiosplus.types.base import SoroushObject


class User(SoroushObject):
    """This object represents a Soroush Plus user or bot."""

    id: int
    is_bot: bool
    first_name: str
    last_name: str | None = None
    username: str | None = None
    language_code: str | None = None
    can_join_groups: bool | None = None
    can_read_all_group_messages: bool | None = None
    supports_inline_queries: bool | None = None

    @property
    def full_name(self) -> str:
        """Full name of the user."""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    @property
    def mention(self) -> str:
        """Username mention or first name if username is absent."""
        if self.username:
            return f"@{self.username}"
        return self.first_name
