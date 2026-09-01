from __future__ import annotations

from aiosplus.types.keyboards import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class InlineKeyboardBuilder:
    """Chainable builder for creating InlineKeyboardMarkup."""

    def __init__(self, markup: InlineKeyboardMarkup | None = None) -> None:
        self._buttons: list[InlineKeyboardButton] = []
        if markup and markup.inline_keyboard:
            for row in markup.inline_keyboard:
                self._buttons.extend(row)
        self._row_sizes: list[int] = []

    def add(self, *buttons: InlineKeyboardButton) -> InlineKeyboardBuilder:
        """Add one or more buttons to the builder."""
        self._buttons.extend(buttons)
        return self

    def button(
        self,
        text: str,
        url: str | None = None,
        callback_data: str | None = None,
    ) -> InlineKeyboardBuilder:
        """Create and add an InlineKeyboardButton."""
        self._buttons.append(
            InlineKeyboardButton(
                text=text,
                url=url,
                callback_data=callback_data,
            )
        )
        return self

    def row(
        self, *buttons: InlineKeyboardButton, width: int | None = None
    ) -> InlineKeyboardBuilder:
        """Add buttons and specify row width."""
        self.add(*buttons)
        if width is not None:
            self._row_sizes.append(width)
        elif buttons:
            self._row_sizes.append(len(buttons))
        return self

    def adjust(self, *sizes: int) -> InlineKeyboardBuilder:
        """Specify layout row sizes (e.g. adjust(2, 1, 3))."""
        self._row_sizes = list(sizes)
        return self

    def as_markup(self) -> InlineKeyboardMarkup:
        """Build and return InlineKeyboardMarkup."""
        if not self._buttons:
            return InlineKeyboardMarkup(inline_keyboard=[])

        if not self._row_sizes:
            # Default to 1 button per row
            return InlineKeyboardMarkup(inline_keyboard=[[btn] for btn in self._buttons])

        rows: list[list[InlineKeyboardButton]] = []
        btn_iter = iter(self._buttons)
        sizes_cycle = list(self._row_sizes)
        size_idx = 0

        while True:
            size = sizes_cycle[size_idx % len(sizes_cycle)]
            row: list[InlineKeyboardButton] = []
            for _ in range(size):
                try:
                    row.append(next(btn_iter))
                except StopIteration:
                    break
            if not row:
                break
            rows.append(row)
            size_idx += 1

        return InlineKeyboardMarkup(inline_keyboard=rows)


class ReplyKeyboardBuilder:
    """Chainable builder for creating ReplyKeyboardMarkup."""

    def __init__(self, markup: ReplyKeyboardMarkup | None = None) -> None:
        self._buttons: list[KeyboardButton] = []
        if markup and markup.keyboard:
            for row in markup.keyboard:
                self._buttons.extend(row)
        self._row_sizes: list[int] = []

    def add(self, *buttons: KeyboardButton | str) -> ReplyKeyboardBuilder:
        """Add one or more buttons to the builder."""
        for b in buttons:
            if isinstance(b, str):
                self._buttons.append(KeyboardButton(text=b))
            else:
                self._buttons.append(b)
        return self

    def button(
        self,
        text: str,
        request_contact: bool | None = None,
        request_location: bool | None = None,
    ) -> ReplyKeyboardBuilder:
        """Create and add a KeyboardButton."""
        self._buttons.append(
            KeyboardButton(
                text=text,
                request_contact=request_contact,
                request_location=request_location,
            )
        )
        return self

    def row(self, *buttons: KeyboardButton | str, width: int | None = None) -> ReplyKeyboardBuilder:
        """Add buttons and specify row width."""
        self.add(*buttons)
        if width is not None:
            self._row_sizes.append(width)
        elif buttons:
            self._row_sizes.append(len(buttons))
        return self

    def adjust(self, *sizes: int) -> ReplyKeyboardBuilder:
        """Specify layout row sizes."""
        self._row_sizes = list(sizes)
        return self

    def as_markup(
        self,
        resize_keyboard: bool = True,
        one_time_keyboard: bool | None = None,
        input_field_placeholder: str | None = None,
    ) -> ReplyKeyboardMarkup:
        """Build and return ReplyKeyboardMarkup."""
        if not self._buttons:
            return ReplyKeyboardMarkup(
                keyboard=[],
                resize_keyboard=resize_keyboard,
                one_time_keyboard=one_time_keyboard,
                input_field_placeholder=input_field_placeholder,
            )

        if not self._row_sizes:
            return ReplyKeyboardMarkup(
                keyboard=[[btn] for btn in self._buttons],
                resize_keyboard=resize_keyboard,
                one_time_keyboard=one_time_keyboard,
                input_field_placeholder=input_field_placeholder,
            )

        rows: list[list[KeyboardButton]] = []
        btn_iter = iter(self._buttons)
        sizes_cycle = list(self._row_sizes)
        size_idx = 0

        while True:
            size = sizes_cycle[size_idx % len(sizes_cycle)]
            row: list[KeyboardButton] = []
            for _ in range(size):
                try:
                    row.append(next(btn_iter))
                except StopIteration:
                    break
            if not row:
                break
            rows.append(row)
            size_idx += 1

        return ReplyKeyboardMarkup(
            keyboard=rows,
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            input_field_placeholder=input_field_placeholder,
        )
