import io
import json
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any, BinaryIO

import httpx

from aiosplus.exceptions import NetworkError, create_api_error

DEFAULT_API_URL = "https://api.splus.ir/bot{token}/{method}"
DEFAULT_FILE_URL = "https://api.splus.ir/file/bot{token}/{file_path}"


class AioSplusSession:
    """HTTP Client session manager for Soroush Plus Bot API requests."""

    def __init__(
        self,
        api_url: str = DEFAULT_API_URL,
        file_url: str = DEFAULT_FILE_URL,
        timeout: float = 60.0,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.api_url = api_url
        self.file_url = file_url
        self.timeout = timeout
        self._client = client
        self._should_close = client is None

    async def get_client(self) -> httpx.AsyncClient:
        """Get or initialize the underlying httpx AsyncClient."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(timeout=httpx.Timeout(self.timeout))
            self._should_close = True
        return self._client

    async def close(self) -> None:
        """Close the underlying client session."""
        if self._client is not None and not self._client.is_closed and self._should_close:
            await self._client.aclose()

    async def __aenter__(self) -> "AioSplusSession":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.close()

    def build_api_url(self, token: str, method: str) -> str:
        """Construct the full API URL for a method."""
        return self.api_url.format(token=token, method=method)

    def build_file_url(self, token: str, file_path: str) -> str:
        """Construct the full download URL for a file path."""
        # Strip leading slash from file_path if present
        cleaned_path = file_path.lstrip("/")
        return self.file_url.format(token=token, file_path=cleaned_path)

    @staticmethod
    def _prepare_value(value: Any) -> Any:
        """Serialize complex objects for form-data or JSON payload."""
        if value is None:
            return None
        if hasattr(value, "model_dump"):
            return value.model_dump(exclude_none=True, by_alias=True)
        if hasattr(value, "dict"):
            return value.dict(exclude_none=True)
        if isinstance(value, (list, tuple)):
            return [AioSplusSession._prepare_value(item) for item in value]
        if isinstance(value, dict):
            return {k: AioSplusSession._prepare_value(v) for k, v in value.items() if v is not None}
        return value

    async def make_request(
        self,
        token: str,
        method: str,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        timeout: float | None = None,
    ) -> Any:
        """Execute an asynchronous API call to Soroush Plus."""
        url = self.build_api_url(token=token, method=method)
        client = await self.get_client()
        req_timeout = timeout or self.timeout

        # Clean payload data
        cleaned_data: dict[str, Any] = {}
        if data:
            for k, v in data.items():
                if v is not None:
                    cleaned_val = self._prepare_value(v)
                    cleaned_data[k] = cleaned_val

        try:
            if files:
                # Multipart/form-data request
                # Serialise nested complex objects into JSON strings for form fields
                form_fields: dict[str, str] = {}
                for k, v in cleaned_data.items():
                    if isinstance(v, (dict, list, bool)):
                        form_fields[k] = json.dumps(v, ensure_ascii=False)
                    else:
                        form_fields[k] = str(v)

                response = await client.post(
                    url,
                    data=form_fields,
                    files=files,
                    timeout=req_timeout,
                )
            else:
                # Standard application/json request
                response = await client.post(
                    url,
                    json=cleaned_data,
                    timeout=req_timeout,
                )
        except httpx.TimeoutException as err:
            raise NetworkError(f"Request to {method} timed out after {req_timeout}s", err) from err
        except httpx.RequestError as err:
            raise NetworkError(f"Network error while connecting to {url}: {err}", err) from err

        return self._process_response(response, method)

    def _process_response(self, response: httpx.Response, method: str) -> Any:
        """Validate status and parse JSON response payload."""
        try:
            result_json = response.json()
        except Exception as err:
            raise NetworkError(
                f"Failed to decode JSON response for {method} (HTTP {response.status_code}): {response.text}",
                err,
            ) from err

        if not isinstance(result_json, dict):
            raise NetworkError(f"Unexpected response format for {method}: {result_json}")

        if not result_json.get("ok"):
            description = result_json.get("description", "Unknown error")
            error_code = result_json.get("error_code", response.status_code)
            parameters = result_json.get("parameters")
            raise create_api_error(error_code, description, parameters)

        return result_json.get("result")

    async def stream_file(
        self,
        token: str,
        file_path: str,
        chunk_size: int = 65536,
    ) -> AsyncGenerator[bytes, None]:
        """Stream bytes of a file from Soroush Plus storage."""
        url = self.build_file_url(token=token, file_path=file_path)
        client = await self.get_client()
        try:
            async with client.stream("GET", url) as response:
                if response.status_code != 200:
                    raise create_api_error(
                        response.status_code,
                        f"Failed to download file: HTTP {response.status_code}",
                    )
                async for chunk in response.aiter_bytes(chunk_size=chunk_size):
                    yield chunk
        except httpx.RequestError as err:
            raise NetworkError(f"Error while downloading file from {url}: {err}", err) from err

    async def download_file(
        self,
        token: str,
        file_path: str,
        destination: str | Path | BinaryIO | io.BytesIO,
        chunk_size: int = 65536,
    ) -> str | Path | BinaryIO | io.BytesIO:
        """Download file and write to disk or binary buffer."""
        if isinstance(destination, (str, Path)):
            dest_path = Path(destination)
            dest_path.parent.mkdir(parents=True, exist_ok=True)
            with open(dest_path, "wb") as f:
                async for chunk in self.stream_file(token, file_path, chunk_size):
                    f.write(chunk)
            return dest_path
        elif hasattr(destination, "write"):
            async for chunk in self.stream_file(token, file_path, chunk_size):
                destination.write(chunk)
            return destination
        else:
            raise ValueError(f"Unsupported destination type: {type(destination)}")
