from __future__ import annotations

import io
from pathlib import Path
from typing import Any, BinaryIO

from aiosplus.bot.context import get_current_bot, set_current_bot
from aiosplus.client.session import AioSplusSession
from aiosplus.enums import ChatAction, ParseMode
from aiosplus.types import (
    BotCommand,
    BotCommandScope,
    BotCommandScopeDefault,
    Chat,
    File,
    ForceReply,
    InlineKeyboardMarkup,
    InputFile,
    InputMedia,
    Message,
    MessageEntity,
    MessageId,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    StickerSet,
    Update,
    User,
    UserProfilePhotos,
    WebhookInfo,
)


class Bot:
    """Soroush Plus Bot API client instance."""

    def __init__(
        self,
        token: str,
        session: AioSplusSession | None = None,
        default_parse_mode: ParseMode | str | None = None,
    ) -> None:
        if not token:
            raise ValueError("Bot token cannot be empty.")
        self.token = token
        self.session = session or AioSplusSession()
        self.default_parse_mode = default_parse_mode
        self._me: User | None = None
        set_current_bot(self)

    @classmethod
    def get_current(cls) -> Bot | None:
        """Get the current active Bot instance in context."""
        return get_current_bot()

    async def __aenter__(self) -> Bot:
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close_session()

    async def close_session(self) -> None:
        """Close the underlying HTTP session."""
        await self.session.close()

    def _resolve_parse_mode(self, parse_mode: str | ParseMode | None) -> str | None:
        if parse_mode is not None:
            return str(parse_mode)
        if self.default_parse_mode is not None:
            return str(self.default_parse_mode)
        return None

    def _prepare_file_field(
        self,
        field_name: str,
        file: str | Path | bytes | BinaryIO | io.BytesIO | InputFile | None,
        data: dict[str, Any],
        files: dict[str, Any],
    ) -> None:
        if file is None:
            return
        if isinstance(file, InputFile):
            if file.file_id is not None:
                data[field_name] = file.file_id
            else:
                files[field_name] = file.to_multipart_tuple()
        elif isinstance(file, (str, Path)):
            p = Path(file)
            if p.is_file():
                inp = InputFile(p)
                files[field_name] = inp.to_multipart_tuple()
            else:
                data[field_name] = str(file)
        elif isinstance(file, (bytes, io.BytesIO)) or hasattr(file, "read"):
            inp = InputFile(file)
            files[field_name] = inp.to_multipart_tuple()

    # --- Authentication & Info ---

    async def get_me(self) -> User:
        """Test bot authentication token and get basic info about the bot."""
        res = await self.session.make_request(self.token, "getMe")
        user = User.model_validate(res).as_bot(self)
        self._me = user
        return user

    async def log_out(self) -> bool:
        """Log out from the cloud Bot API server."""
        res = await self.session.make_request(self.token, "logOut")
        return bool(res)

    async def close(self) -> bool:
        """Close the bot instance before moving it between servers."""
        res = await self.session.make_request(self.token, "close")
        return bool(res)

    # --- Updates & Webhooks ---

    async def get_updates(
        self,
        offset: int | None = None,
        limit: int | None = None,
        timeout: int | None = None,
        allowed_updates: list[str] | None = None,
    ) -> list[Update]:
        """Receive incoming updates using Long Polling."""
        payload: dict[str, Any] = {
            "offset": offset,
            "limit": limit,
            "timeout": timeout,
            "allowed_updates": allowed_updates,
        }
        res = await self.session.make_request(
            self.token,
            "getUpdates",
            data=payload,
            timeout=float(timeout + 15) if timeout else None,
        )
        updates: list[Update] = []
        if isinstance(res, list):
            for item in res:
                u = Update.model_validate(item).as_bot(self)
                if u.event:
                    u.event.as_bot(self)
                updates.append(u)
        return updates

    async def set_webhook(
        self,
        url: str,
        certificate: str | Path | bytes | BinaryIO | io.BytesIO | InputFile | None = None,
        ip_address: str | None = None,
        max_connections: int | None = None,
        allowed_updates: list[str] | None = None,
        drop_pending_updates: bool | None = None,
    ) -> bool:
        """Specify a URL to receive incoming updates via an outgoing webhook."""
        data: dict[str, Any] = {
            "url": url,
            "ip_address": ip_address,
            "max_connections": max_connections,
            "allowed_updates": allowed_updates,
            "drop_pending_updates": drop_pending_updates,
        }
        files: dict[str, Any] = {}
        self._prepare_file_field("certificate", certificate, data, files)
        res = await self.session.make_request(
            self.token, "setWebhook", data=data, files=files or None
        )
        return bool(res)

    async def delete_webhook(self, drop_pending_updates: bool | None = None) -> bool:
        """Remove webhook integration."""
        payload = {"drop_pending_updates": drop_pending_updates}
        res = await self.session.make_request(self.token, "deleteWebhook", data=payload)
        return bool(res)

    async def get_webhook_info(self) -> WebhookInfo:
        """Get current webhook status."""
        res = await self.session.make_request(self.token, "getWebhookInfo")
        return WebhookInfo.model_validate(res).as_bot(self)

    # --- Sending Messages & Media ---

    async def send_message(
        self,
        chat_id: int | str,
        text: str,
        parse_mode: str | ParseMode | None = None,
        entities: list[MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
        reply_to_message_id: int | None = None,
        allow_sending_without_reply: bool | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send a text message."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": self._resolve_parse_mode(parse_mode),
            "entities": entities,
            "disable_web_page_preview": disable_web_page_preview,
            "reply_to_message_id": reply_to_message_id,
            "allow_sending_without_reply": allow_sending_without_reply,
            "reply_markup": reply_markup,
        }
        res = await self.session.make_request(self.token, "sendMessage", data=payload)
        return Message.model_validate(res).as_bot(self)

    async def forward_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
    ) -> Message:
        """Forward a message of any kind."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id,
        }
        res = await self.session.make_request(self.token, "forwardMessage", data=payload)
        return Message.model_validate(res).as_bot(self)

    async def copy_message(
        self,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        caption: str | None = None,
        parse_mode: str | ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> MessageId:
        """Copy a message of any kind without link to the original."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "from_chat_id": from_chat_id,
            "message_id": message_id,
            "caption": caption,
            "parse_mode": self._resolve_parse_mode(parse_mode),
            "caption_entities": caption_entities,
            "reply_markup": reply_markup,
        }
        res = await self.session.make_request(self.token, "copyMessage", data=payload)
        return MessageId.model_validate(res).as_bot(self)

    async def send_photo(
        self,
        chat_id: int | str,
        photo: str | Path | bytes | BinaryIO | io.BytesIO | InputFile,
        caption: str | None = None,
        parse_mode: str | ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send a photo."""
        data: dict[str, Any] = {
            "chat_id": chat_id,
            "caption": caption,
            "parse_mode": self._resolve_parse_mode(parse_mode),
            "caption_entities": caption_entities,
            "reply_markup": reply_markup,
        }
        files: dict[str, Any] = {}
        self._prepare_file_field("photo", photo, data, files)
        res = await self.session.make_request(
            self.token, "sendPhoto", data=data, files=files or None
        )
        return Message.model_validate(res).as_bot(self)

    async def send_audio(
        self,
        chat_id: int | str,
        audio: str | Path | bytes | BinaryIO | io.BytesIO | InputFile,
        caption: str | None = None,
        parse_mode: str | ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: int | None = None,
        performer: str | None = None,
        title: str | None = None,
        thumb: str | Path | bytes | BinaryIO | io.BytesIO | InputFile | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send an audio file."""
        data: dict[str, Any] = {
            "chat_id": chat_id,
            "caption": caption,
            "parse_mode": self._resolve_parse_mode(parse_mode),
            "caption_entities": caption_entities,
            "duration": duration,
            "performer": performer,
            "title": title,
            "reply_markup": reply_markup,
        }
        files: dict[str, Any] = {}
        self._prepare_file_field("audio", audio, data, files)
        self._prepare_file_field("thumb", thumb, data, files)
        res = await self.session.make_request(
            self.token, "sendAudio", data=data, files=files or None
        )
        return Message.model_validate(res).as_bot(self)

    async def send_document(
        self,
        chat_id: int | str,
        document: str | Path | bytes | BinaryIO | io.BytesIO | InputFile,
        thumb: str | Path | bytes | BinaryIO | io.BytesIO | InputFile | None = None,
        caption: str | None = None,
        parse_mode: str | ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        disable_content_type_detection: bool | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send a general document file."""
        data: dict[str, Any] = {
            "chat_id": chat_id,
            "caption": caption,
            "parse_mode": self._resolve_parse_mode(parse_mode),
            "caption_entities": caption_entities,
            "disable_content_type_detection": disable_content_type_detection,
            "reply_markup": reply_markup,
        }
        files: dict[str, Any] = {}
        self._prepare_file_field("document", document, data, files)
        self._prepare_file_field("thumb", thumb, data, files)
        res = await self.session.make_request(
            self.token, "sendDocument", data=data, files=files or None
        )
        return Message.model_validate(res).as_bot(self)

    async def send_video(
        self,
        chat_id: int | str,
        video: str | Path | bytes | BinaryIO | io.BytesIO | InputFile,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumb: str | Path | bytes | BinaryIO | io.BytesIO | InputFile | None = None,
        caption: str | None = None,
        parse_mode: str | ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        supports_streaming: bool | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send a video file."""
        data: dict[str, Any] = {
            "chat_id": chat_id,
            "duration": duration,
            "width": width,
            "height": height,
            "caption": caption,
            "parse_mode": self._resolve_parse_mode(parse_mode),
            "caption_entities": caption_entities,
            "supports_streaming": supports_streaming,
            "reply_markup": reply_markup,
        }
        files: dict[str, Any] = {}
        self._prepare_file_field("video", video, data, files)
        self._prepare_file_field("thumb", thumb, data, files)
        res = await self.session.make_request(
            self.token, "sendVideo", data=data, files=files or None
        )
        return Message.model_validate(res).as_bot(self)

    async def send_animation(
        self,
        chat_id: int | str,
        animation: str | Path | bytes | BinaryIO | io.BytesIO | InputFile,
        duration: int | None = None,
        width: int | None = None,
        height: int | None = None,
        thumb: str | Path | bytes | BinaryIO | io.BytesIO | InputFile | None = None,
        caption: str | None = None,
        parse_mode: str | ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send an animation (GIF or silent video)."""
        data: dict[str, Any] = {
            "chat_id": chat_id,
            "duration": duration,
            "width": width,
            "height": height,
            "caption": caption,
            "parse_mode": self._resolve_parse_mode(parse_mode),
            "caption_entities": caption_entities,
            "reply_markup": reply_markup,
        }
        files: dict[str, Any] = {}
        self._prepare_file_field("animation", animation, data, files)
        self._prepare_file_field("thumb", thumb, data, files)
        res = await self.session.make_request(
            self.token, "sendAnimation", data=data, files=files or None
        )
        return Message.model_validate(res).as_bot(self)

    async def send_voice(
        self,
        chat_id: int | str,
        voice: str | Path | bytes | BinaryIO | io.BytesIO | InputFile,
        caption: str | None = None,
        parse_mode: str | ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        duration: int | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send a voice note."""
        data: dict[str, Any] = {
            "chat_id": chat_id,
            "caption": caption,
            "parse_mode": self._resolve_parse_mode(parse_mode),
            "caption_entities": caption_entities,
            "duration": duration,
            "reply_markup": reply_markup,
        }
        files: dict[str, Any] = {}
        self._prepare_file_field("voice", voice, data, files)
        res = await self.session.make_request(
            self.token, "sendVoice", data=data, files=files or None
        )
        return Message.model_validate(res).as_bot(self)

    async def send_video_note(
        self,
        chat_id: int | str,
        video_note: str | Path | bytes | BinaryIO | io.BytesIO | InputFile,
        duration: int | None = None,
        length: int | None = None,
        thumb: str | Path | bytes | BinaryIO | io.BytesIO | InputFile | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send a round video note."""
        data: dict[str, Any] = {
            "chat_id": chat_id,
            "duration": duration,
            "length": length,
            "reply_markup": reply_markup,
        }
        files: dict[str, Any] = {}
        self._prepare_file_field("video_note", video_note, data, files)
        self._prepare_file_field("thumb", thumb, data, files)
        res = await self.session.make_request(
            self.token, "sendVideoNote", data=data, files=files or None
        )
        return Message.model_validate(res).as_bot(self)

    async def send_media_group(
        self,
        chat_id: int | str,
        media: list[InputMedia],
    ) -> list[Message]:
        """Send a group of photos, videos, documents, or audios as an album."""
        files: dict[str, Any] = {}
        media_payload: list[dict[str, Any]] = []

        for idx, item in enumerate(media):
            item_dict = item.model_dump(exclude_none=True)
            attach_name = f"file_{idx}"
            if isinstance(item.media, InputFile) and item.media.file_id is None:
                files[attach_name] = item.media.to_multipart_tuple()
                item_dict["media"] = f"attach://{attach_name}"
            elif isinstance(item.media, (Path, str)):
                p = Path(item.media)
                if p.is_file():
                    files[attach_name] = InputFile(p).to_multipart_tuple()
                    item_dict["media"] = f"attach://{attach_name}"
            media_payload.append(item_dict)

        data = {
            "chat_id": chat_id,
            "media": media_payload,
        }
        res = await self.session.make_request(
            self.token, "sendMediaGroup", data=data, files=files or None
        )
        messages: list[Message] = []
        if isinstance(res, list):
            for m in res:
                messages.append(Message.model_validate(m).as_bot(self))
        return messages

    async def send_location(
        self,
        chat_id: int | str,
        latitude: float,
        longitude: float,
        horizontal_accuracy: float | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send point on the map."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "latitude": latitude,
            "longitude": longitude,
            "horizontal_accuracy": horizontal_accuracy,
            "reply_markup": reply_markup,
        }
        res = await self.session.make_request(self.token, "sendLocation", data=payload)
        return Message.model_validate(res).as_bot(self)

    async def send_contact(
        self,
        chat_id: int | str,
        phone_number: str,
        first_name: str,
        last_name: str | None = None,
        vcard: str | None = None,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send phone contacts."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "phone_number": phone_number,
            "first_name": first_name,
            "last_name": last_name,
            "vcard": vcard,
            "reply_markup": reply_markup,
        }
        res = await self.session.make_request(self.token, "sendContact", data=payload)
        return Message.model_validate(res).as_bot(self)

    async def send_sticker(
        self,
        chat_id: int | str,
        sticker: str | Path | bytes | BinaryIO | io.BytesIO | InputFile,
        reply_markup: InlineKeyboardMarkup
        | ReplyKeyboardMarkup
        | ReplyKeyboardRemove
        | ForceReply
        | None = None,
    ) -> Message:
        """Send static or animated sticker."""
        data: dict[str, Any] = {
            "chat_id": chat_id,
            "reply_markup": reply_markup,
        }
        files: dict[str, Any] = {}
        self._prepare_file_field("sticker", sticker, data, files)
        res = await self.session.make_request(
            self.token, "sendSticker", data=data, files=files or None
        )
        return Message.model_validate(res).as_bot(self)

    # --- Chat Actions & Status ---

    async def send_chat_action(
        self,
        chat_id: int | str,
        action: ChatAction | str,
    ) -> bool:
        """Broadcast chat status (typing, upload_photo, etc.)."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "action": str(action),
        }
        res = await self.session.make_request(self.token, "sendChatAction", data=payload)
        return bool(res)

    async def get_user_profile_photos(
        self,
        user_id: int,
        offset: int | None = None,
        limit: int | None = None,
    ) -> UserProfilePhotos:
        """Get list of profile photos for a user."""
        payload: dict[str, Any] = {
            "user_id": user_id,
            "offset": offset,
            "limit": limit,
        }
        res = await self.session.make_request(self.token, "getUserProfilePhotos", data=payload)
        return UserProfilePhotos.model_validate(res).as_bot(self)

    async def get_file(self, file_id: str) -> File:
        """Get basic info about a file and prepare it for downloading."""
        payload = {"file_id": file_id}
        res = await self.session.make_request(self.token, "getFile", data=payload)
        return File.model_validate(res).as_bot(self)

    async def download_file(
        self,
        file_path_or_file: str | File,
        destination: str | Path | BinaryIO | io.BytesIO,
        chunk_size: int = 65536,
    ) -> str | Path | BinaryIO | io.BytesIO:
        """Download file content from Soroush Plus servers."""
        if isinstance(file_path_or_file, File):
            if not file_path_or_file.file_path:
                raise ValueError("File object has no file_path.")
            file_path = file_path_or_file.file_path
        else:
            file_path = str(file_path_or_file)

        return await self.session.download_file(
            token=self.token,
            file_path=file_path,
            destination=destination,
            chunk_size=chunk_size,
        )

    async def pin_chat_message(
        self,
        chat_id: int | str,
        message_id: int,
    ) -> bool:
        """Pin a message in a chat."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        res = await self.session.make_request(self.token, "pinChatMessage", data=payload)
        return bool(res)

    async def unpin_chat_message(
        self,
        chat_id: int | str,
        message_id: int | None = None,
    ) -> bool:
        """Unpin a message in a chat."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        res = await self.session.make_request(self.token, "unpinChatMessage", data=payload)
        return bool(res)

    async def get_chat(self, chat_id: int | str) -> Chat:
        """Get up-to-date information about the chat."""
        payload = {"chat_id": chat_id}
        res = await self.session.make_request(self.token, "getChat", data=payload)
        return Chat.model_validate(res).as_bot(self)

    # --- Callbacks ---

    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: str | None = None,
        show_alert: bool | None = None,
        url: str | None = None,
        cache_time: int | None = None,
    ) -> bool:
        """Send answer to callback queries sent from inline keyboards."""
        payload: dict[str, Any] = {
            "callback_query_id": callback_query_id,
            "text": text,
            "show_alert": show_alert,
            "url": url,
            "cache_time": cache_time,
        }
        res = await self.session.make_request(self.token, "answerCallbackQuery", data=payload)
        return bool(res)

    # --- Bot Commands ---

    async def set_my_commands(
        self,
        commands: list[BotCommand],
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
    ) -> bool:
        """Change the list of the bot's commands."""
        payload: dict[str, Any] = {
            "commands": commands,
            "scope": scope or BotCommandScopeDefault(),
            "language_code": language_code,
        }
        res = await self.session.make_request(self.token, "setMyCommands", data=payload)
        return bool(res)

    async def delete_my_commands(
        self,
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
    ) -> bool:
        """Delete the list of the bot's commands."""
        payload: dict[str, Any] = {
            "scope": scope,
            "language_code": language_code,
        }
        res = await self.session.make_request(self.token, "deleteMyCommands", data=payload)
        return bool(res)

    async def get_my_commands(
        self,
        scope: BotCommandScope | None = None,
        language_code: str | None = None,
    ) -> list[BotCommand]:
        """Get the current list of the bot's commands."""
        payload: dict[str, Any] = {
            "scope": scope,
            "language_code": language_code,
        }
        res = await self.session.make_request(self.token, "getMyCommands", data=payload)
        commands: list[BotCommand] = []
        if isinstance(res, list):
            for item in res:
                commands.append(BotCommand.model_validate(item).as_bot(self))
        return commands

    # --- Message Editing & Deleting ---

    async def edit_message_text(
        self,
        text: str,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        parse_mode: str | ParseMode | None = None,
        entities: list[MessageEntity] | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
        disable_web_page_preview: bool | None = None,
    ) -> Message | bool:
        """Edit text and game messages."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
            "text": text,
            "parse_mode": self._resolve_parse_mode(parse_mode),
            "entities": entities,
            "reply_markup": reply_markup,
            "disable_web_page_preview": disable_web_page_preview,
        }
        res = await self.session.make_request(self.token, "editMessageText", data=payload)
        if isinstance(res, dict):
            return Message.model_validate(res).as_bot(self)
        return bool(res)

    async def edit_message_caption(
        self,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        caption: str | None = None,
        parse_mode: str | ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Edit caption of messages."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
            "caption": caption,
            "parse_mode": self._resolve_parse_mode(parse_mode),
            "caption_entities": caption_entities,
            "reply_markup": reply_markup,
        }
        res = await self.session.make_request(self.token, "editMessageCaption", data=payload)
        if isinstance(res, dict):
            return Message.model_validate(res).as_bot(self)
        return bool(res)

    async def edit_message_media(
        self,
        media: InputMedia,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Edit animation, audio, document, photo, or video messages."""
        files: dict[str, Any] = {}
        item_dict = media.model_dump(exclude_none=True)
        if isinstance(media.media, InputFile) and media.media.file_id is None:
            files["media_file"] = media.media.to_multipart_tuple()
            item_dict["media"] = "attach://media_file"

        data: dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
            "media": item_dict,
            "reply_markup": reply_markup,
        }
        res = await self.session.make_request(
            self.token, "editMessageMedia", data=data, files=files or None
        )
        if isinstance(res, dict):
            return Message.model_validate(res).as_bot(self)
        return bool(res)

    async def edit_message_reply_markup(
        self,
        chat_id: int | str | None = None,
        message_id: int | None = None,
        reply_markup: InlineKeyboardMarkup | None = None,
    ) -> Message | bool:
        """Edit only the reply markup of messages."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
            "reply_markup": reply_markup,
        }
        res = await self.session.make_request(self.token, "editMessageReplyMarkup", data=payload)
        if isinstance(res, dict):
            return Message.model_validate(res).as_bot(self)
        return bool(res)

    async def delete_message(
        self,
        chat_id: int | str,
        message_id: int,
    ) -> bool:
        """Delete a message."""
        payload: dict[str, Any] = {
            "chat_id": chat_id,
            "message_id": message_id,
        }
        res = await self.session.make_request(self.token, "deleteMessage", data=payload)
        return bool(res)

    async def get_sticker_set(self, name: str) -> StickerSet:
        """Get a sticker set by name."""
        payload = {"name": name}
        res = await self.session.make_request(self.token, "getStickerSet", data=payload)
        return StickerSet.model_validate(res).as_bot(self)
