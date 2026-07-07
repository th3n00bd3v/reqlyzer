from pydantic import BaseModel, Field


class Metadata(BaseModel):
    """
    Technical metadata extracted from a request.
    """

    scheme: str = ""

    host: str = ""

    path: str = ""

    method: str = ""

    content_type: str = ""

    mime_type: str = ""

    request_size: int = 0

    response_size: int = 0

    response_time_ms: float = 0.0

    status_code: int = 0

    server_ip: str | None = None

    has_query_parameters: bool = False

    has_cookies: bool = False

    has_request_body: bool = False

    query_parameter_count: int = 0

    header_count: int = 0

    cookie_count: int = 0

    technologies: list[str] = Field(default_factory=list)