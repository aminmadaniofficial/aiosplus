import io
from pathlib import Path

import httpx
import pytest

from aiosplus.client.session import AioSplusSession
from aiosplus.enums import (
    ChatAction,
    ChatType,
    MessageEntityType,
    ParseMode,
)
from aiosplus.exceptions import (
    SoroushAPIError,
    SoroushBadRequest,
    SoroushConflictError,
    SoroushFloodError,
    SoroushForbidden,
    SoroushNotFound,
    SoroushServerError,
    SoroushUnauthorized,
    create_api_error,
)


def test_enums() -> None:
    assert str(ParseMode.MARKDOWN_V2) == "MarkdownV2"
    assert str(ParseMode.HTML) == "HTML"
    assert str(ParseMode.MARKDOWN) == "Markdown"
    assert ChatType.PRIVATE == "private"
    assert MessageEntityType.BOLD == "bold"
    assert ChatAction.TYPING == "typing"


def test_exceptions_hierarchy() -> None:
    err_400 = create_api_error(400, "Bad Request: chat not found")
    assert isinstance(err_400, SoroushBadRequest)
    assert err_400.error_code == 400

    err_401 = create_api_error(401, "Unauthorized: token is invalid")
    assert isinstance(err_401, SoroushUnauthorized)

    err_403 = create_api_error(403, "Forbidden: bot blocked by user")
    assert isinstance(err_403, SoroushForbidden)

    err_404 = create_api_error(404, "Not Found: method getUnknown not found")
    assert isinstance(err_404, SoroushNotFound)

    err_409 = create_api_error(409, "Conflict: terminated by other getUpdates")
    assert isinstance(err_409, SoroushConflictError)

    err_429 = create_api_error(
        429, "Too Many Requests: retry after 5", parameters={"retry_after": 5}
    )
    assert isinstance(err_429, SoroushFloodError)
    assert err_429.retry_after == 5

    err_502 = create_api_error(502, "Bad Gateway")
    assert isinstance(err_502, SoroushServerError)

    err_custom = create_api_error(418, "I'm a teapot")
    assert type(err_custom) is SoroushAPIError


@pytest.mark.asyncio
async def test_session_urls() -> None:
    session = AioSplusSession()
    api_url = session.build_api_url("123:ABC", "getMe")
    assert api_url == "https://api.splus.ir/bot123:ABC/getMe"

    file_url = session.build_file_url("123:ABC", "photos/file_1.jpg")
    assert file_url == "https://api.splus.ir/file/bot123:ABC/photos/file_1.jpg"

    file_url_slash = session.build_file_url("123:ABC", "/documents/file_2.pdf")
    assert file_url_slash == "https://api.splus.ir/file/bot123:ABC/documents/file_2.pdf"
    await session.close()


@pytest.mark.asyncio
async def test_session_mock_request_success() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://api.splus.ir/bot123:ABC/getMe"
        return httpx.Response(
            200,
            json={"ok": True, "result": {"id": 123456, "is_bot": True, "first_name": "TestBot"}},
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        session = AioSplusSession(client=mock_client)
        result = await session.make_request("123:ABC", "getMe")
        assert result["id"] == 123456
        assert result["is_bot"] is True


@pytest.mark.asyncio
async def test_session_mock_request_error() -> None:
    def handler(_request: httpx.Request) -> httpx.Response:
        return httpx.Response(
            400, json={"ok": False, "error_code": 400, "description": "Chat not found"}
        )

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        session = AioSplusSession(client=mock_client)
        with pytest.raises(SoroushBadRequest) as exc_info:
            await session.make_request("123:ABC", "sendMessage", {"chat_id": 9999, "text": "Hi"})
        assert exc_info.value.error_code == 400
        assert "Chat not found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_session_download_file(tmp_path: Path) -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url == "https://api.splus.ir/file/bot123:ABC/files/test.txt"
        return httpx.Response(200, content=b"Hello Soroush Plus File Content")

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as mock_client:
        session = AioSplusSession(client=mock_client)
        # Test download to Path
        dest_file = tmp_path / "downloaded.txt"
        saved_path = await session.download_file("123:ABC", "files/test.txt", dest_file)
        assert isinstance(saved_path, Path)
        assert dest_file.read_bytes() == b"Hello Soroush Plus File Content"

        # Test download to BytesIO
        buf = io.BytesIO()
        await session.download_file("123:ABC", "files/test.txt", buf)
        assert buf.getvalue() == b"Hello Soroush Plus File Content"
