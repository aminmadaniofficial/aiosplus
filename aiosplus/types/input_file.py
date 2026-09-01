import io
import mimetypes
from pathlib import Path
from typing import BinaryIO


class InputFile:
    """Represents a file to be uploaded to Soroush Plus."""

    def __init__(
        self,
        file: str | Path | bytes | BinaryIO | io.BytesIO,
        filename: str | None = None,
        chunk_size: int = 65536,
    ) -> None:
        self.chunk_size = chunk_size
        self._custom_filename = filename
        self.filename: str = "file.bin"
        self.file_path: Path | None = None
        self.data: bytes | BinaryIO | io.BytesIO | None = None
        self.file_id: str | None = None

        if isinstance(file, (str, Path)):
            path = Path(file)
            if path.is_file():
                self.file_path = path
                self.filename = filename or path.name
            else:
                # If it is a string representing a remote file_id or non-existent path
                self.filename = filename or str(file)
                self.file_id = str(file)
        elif isinstance(file, bytes):
            self.data = file
            self.filename = filename or "file.bin"
        elif hasattr(file, "read"):
            self.data = file
            name_attr = getattr(file, "name", None)
            if name_attr and isinstance(name_attr, (str, Path)):
                self.filename = filename or Path(name_attr).name
            else:
                self.filename = filename or "file.bin"
        else:
            raise ValueError(f"Unsupported file type for InputFile: {type(file)}")

    @property
    def content_type(self) -> str:
        """Guess mime type from filename."""
        mime, _ = mimetypes.guess_type(self.filename)
        return mime or "application/octet-stream"

    def read_bytes(self) -> bytes:
        """Read full binary content of the file."""
        if self.file_path is not None:
            return self.file_path.read_bytes()
        if isinstance(self.data, bytes):
            return self.data
        if self.data is not None and hasattr(self.data, "read"):
            pos = getattr(self.data, "tell", lambda: None)()
            if pos is not None and pos != 0:
                self.data.seek(0)
            content = self.data.read()
            if isinstance(content, str):
                return content.encode("utf-8")
            if isinstance(content, bytes):
                return content
        return b""

    def to_multipart_tuple(self) -> tuple[str, bytes, str]:
        """Convert to (filename, data, content_type) for httpx files param."""
        return (self.filename, self.read_bytes(), self.content_type)
