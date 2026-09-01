from __future__ import annotations

import re
from collections.abc import Sequence
from dataclasses import dataclass
from re import Pattern
from typing import Any

from aiosplus.filters.base import BaseFilter
from aiosplus.types.message import Message


@dataclass
class CommandObject:
    """Represents parsed command data."""

    prefix: str
    command: str
    args: str | None
    mention: str | None

    @property
    def deep_link(self) -> str | None:
        """Deep linking argument (same as args)."""
        return self.args

    @property
    def text(self) -> str:
        """Full text of command with arguments."""
        if self.args:
            return f"{self.prefix}{self.command} {self.args}"
        return f"{self.prefix}{self.command}"


class Command(BaseFilter):
    """Filter to match bot commands (e.g. /start, /help)."""

    def __init__(
        self,
        commands: str | Sequence[str],
        prefix: str = "/",
        ignore_case: bool = True,
        ignore_mention: bool = False,
    ) -> None:
        if isinstance(commands, str):
            self.commands = [commands.lower() if ignore_case else commands]
        else:
            self.commands = [c.lower() if ignore_case else c for c in commands]

        self.prefix = prefix
        self.ignore_case = ignore_case
        self.ignore_mention = ignore_mention
        self._pattern = re.compile(
            rf"^(?P<prefix>{re.escape(prefix)})(?P<command>[a-zA-Z0-9_]+)(?:@(?P<mention>[a-zA-Z0-9_]+))?(?:\s+(?P<args>[\s\S]*))?$"
        )

    async def __call__(self, event: Any, **kwargs: Any) -> bool | dict[str, Any]:
        if not isinstance(event, Message) or not event.text:
            return False

        text = event.text.strip()
        match = self._pattern.match(text)
        if not match:
            return False

        prefix = match.group("prefix")
        command = match.group("command")
        mention = match.group("mention")
        args = match.group("args")

        cmd_to_check = command.lower() if self.ignore_case else command
        if cmd_to_check not in self.commands:
            return False

        # If mention is present and bot is in context, verify mention
        bot = kwargs.get("bot")
        if mention and not self.ignore_mention and bot and bot._me and bot._me.username:
            if mention.lower() != bot._me.username.lower():
                return False

        cmd_obj = CommandObject(
            prefix=prefix,
            command=command,
            args=args.strip() if args else None,
            mention=mention,
        )
        return {"command": cmd_obj}


class CommandStart(Command):
    """Filter shortcut to match /start command with optional deep link argument validation."""

    def __init__(
        self,
        deep_link: str | Pattern[str] | None = None,
        prefix: str = "/",
        ignore_case: bool = True,
        ignore_mention: bool = False,
    ) -> None:
        super().__init__(
            commands="start",
            prefix=prefix,
            ignore_case=ignore_case,
            ignore_mention=ignore_mention,
        )
        self.deep_link_pattern = re.compile(deep_link) if isinstance(deep_link, str) else deep_link

    async def __call__(self, event: Any, **kwargs: Any) -> bool | dict[str, Any]:
        res = await super().__call__(event, **kwargs)
        if not res or not isinstance(res, dict):
            return False

        if self.deep_link_pattern is not None:
            cmd_obj: CommandObject = res["command"]
            if not cmd_obj.args:
                return False
            if not self.deep_link_pattern.search(cmd_obj.args):
                return False

        return res


class CommandHelp(Command):
    """Filter shortcut to match /help command."""

    def __init__(
        self,
        prefix: str = "/",
        ignore_case: bool = True,
        ignore_mention: bool = False,
    ) -> None:
        super().__init__(
            commands="help",
            prefix=prefix,
            ignore_case=ignore_case,
            ignore_mention=ignore_mention,
        )
