import json
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from models.metadata import Metadata
from models.request import AnalyzedRequest


class HARParser:
    """
    Parses HAR files into Reqlyzer's normalized request model.
    """

    def __init__(self, file_path: str | Path):
        self.file_path = Path(file_path)

    def parse(self) -> list[AnalyzedRequest]:
        """
        Reads the HAR file and returns a list of AnalyzedRequest objects.
        """

        if not self.file_path.exists():
            raise FileNotFoundError(f"HAR file not found: {self.file_path}")

        with self.file_path.open("r", encoding="utf-8") as file:
            har_data = json.load(file)

        log = har_data.get("log", {})
        entries = log.get("entries", [])

        parsed_requests: list[AnalyzedRequest] = []

        for index, entry in enumerate(entries, start=1):

            request = entry.get("request", {})
            response = entry.get("response", {})
            content = response.get("content", {})

            parsed_url = urlparse(request.get("url", ""))
            query_params = parse_qs(parsed_url.query)

            headers = {
                header.get("name"): header.get("value")
                for header in request.get("headers", [])
            }

            response_headers = {
                header.get("name"): header.get("value")
                for header in response.get("headers", [])
            }

            cookies = [
                cookie.get("name")
                for cookie in request.get("cookies", [])
            ]

            request_body = None

            post_data = request.get("postData")
            if post_data:
                request_body = post_data.get("text")

            analyzed_request = AnalyzedRequest(
                # -------------------------------------------------
                # Basic Request Information
                # -------------------------------------------------
                id=index,
                method=request.get("method", ""),
                url=request.get("url", ""),
                scheme=parsed_url.scheme,
                host=parsed_url.netloc,
                path=parsed_url.path,
                query_params=query_params,
                headers=headers,
                cookies=cookies,
                request_body=request_body,

                # -------------------------------------------------
                # Response Information
                # -------------------------------------------------
                status_code=response.get("status"),
                status_text=response.get("statusText"),
                response_headers=response_headers,
                response_size=content.get("size"),
                mime_type=content.get("mimeType"),
                response_time_ms=entry.get("time"),
                started_date_time=entry.get("startedDateTime"),
                server_ip=entry.get("serverIPAddress"),

                # -------------------------------------------------
                # Initial Metadata
                # -------------------------------------------------
                metadata=Metadata(
                    scheme=parsed_url.scheme,
                    host=parsed_url.netloc,
                    path=parsed_url.path,
                    method=request.get("method", ""),
                    content_type=headers.get("Content-Type", ""),
                    mime_type=content.get("mimeType") or "",
                    request_size=len(request_body) if request_body else 0,
                    response_size=content.get("size") or 0,
                    response_time_ms=entry.get("time") or 0.0,
                    status_code=response.get("status") or 0,
                    server_ip=entry.get("serverIPAddress"),
                    has_query_parameters=bool(query_params),
                    has_cookies=bool(cookies),
                    has_request_body=bool(request_body),
                    query_parameter_count=len(query_params),
                    header_count=len(headers),
                    cookie_count=len(cookies),
                ),
            )

            parsed_requests.append(analyzed_request)

        return parsed_requests