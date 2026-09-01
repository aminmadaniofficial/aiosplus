from aiosplus.types.base import SoroushObject


class ResponseParameters(SoroushObject):
    """Describes why a request was unsuccessful."""

    retry_after: int | None = None


class WebhookInfo(SoroushObject):
    """Describes the current status of a webhook."""

    url: str
    has_custom_certificate: bool
    pending_update_count: int
    ip_address: str | None = None
    last_error_date: int | None = None
    last_error_message: str | None = None
    max_connections: int | None = None
    allowed_updates: list[str] | None = None
