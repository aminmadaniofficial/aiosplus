from __future__ import annotations

import html
import re

MD_V2_RESERVED = r"([_\*\[\]\(\)~`>#\+\-=\|{}\.!\\/])"


def escape_md(text: str) -> str:
    """Escape text for MarkdownV2 parse mode in Soroush Plus."""
    return re.sub(MD_V2_RESERVED, r"\\\1", text)


def escape_html(text: str) -> str:
    """Escape text for HTML parse mode."""
    return html.escape(text, quote=True)


def bold(text: str, parse_mode: str = "HTML") -> str:
    """Wrap text in bold tags."""
    if parse_mode.lower() == "html":
        return f"<b>{escape_html(text)}</b>"
    return f"*{escape_md(text)}*"


def italic(text: str, parse_mode: str = "HTML") -> str:
    """Wrap text in italic tags."""
    if parse_mode.lower() == "html":
        return f"<i>{escape_html(text)}</i>"
    return f"_{escape_md(text)}_"


def underline(text: str, parse_mode: str = "HTML") -> str:
    """Wrap text in underline tags."""
    if parse_mode.lower() == "html":
        return f"<u>{escape_html(text)}</u>"
    return f"__{escape_md(text)}__"


def strikethrough(text: str, parse_mode: str = "HTML") -> str:
    """Wrap text in strikethrough tags."""
    if parse_mode.lower() == "html":
        return f"<s>{escape_html(text)}</s>"
    return f"~{escape_md(text)}~"


def spoiler(text: str, parse_mode: str = "HTML") -> str:
    """Wrap text in spoiler tags."""
    if parse_mode.lower() == "html":
        return f'<span class="tg-spoiler">{escape_html(text)}</span>'
    return f"||{escape_md(text)}||"


def code(text: str, parse_mode: str = "HTML") -> str:
    """Wrap inline fixed-width code."""
    if parse_mode.lower() == "html":
        return f"<code>{escape_html(text)}</code>"
    escaped = text.replace("\\", "\\\\").replace("`", "\\`")
    return f"`{escaped}`"


def pre(text: str, language: str = "", parse_mode: str = "HTML") -> str:
    """Wrap preformatted code block with optional language."""
    if parse_mode.lower() == "html":
        if language:
            return f'<pre><code class="language-{escape_html(language)}">{escape_html(text)}</code></pre>'
        return f"<pre>{escape_html(text)}</pre>"
    escaped = text.replace("\\", "\\\\").replace("`", "\\`")
    if language:
        return f"```{language}\n{escaped}\n```"
    return f"```\n{escaped}\n```"


def link(title: str, url: str, parse_mode: str = "HTML") -> str:
    """Create a clickable link."""
    if parse_mode.lower() == "html":
        return f'<a href="{escape_html(url)}">{escape_html(title)}</a>'
    escaped_url = url.replace("\\", "\\\\").replace(")", "\\)")
    return f"[{escape_md(title)}]({escaped_url})"


def blockquote(text: str, expandable: bool = False, parse_mode: str = "HTML") -> str:
    """Wrap text in block quotation."""
    if parse_mode.lower() == "html":
        tag = "<blockquote expandable>" if expandable else "<blockquote>"
        return f"{tag}{escape_html(text)}</blockquote>"
    prefix = ">" if not expandable else "**>"
    lines = text.split("\n")
    return "\n".join(f"{prefix}{escape_md(line)}" for line in lines)
