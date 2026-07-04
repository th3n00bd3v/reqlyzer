import json
from pathlib import Path
from urllib.parse import urlparse, parse_qs


class HARParser:
    """
    Parses HAR files into Reqlyzer's normalized request model.
    """

    def __init__(self, file_path):
        self.file_path = Path(file_path)

    def parse(self):
        """
        Reads the HAR file and returns a list of normalized requests.
        """
        if not self.file_path.exists():
            raise FileNotFoundError(f"HAR file not found: {self.file_path}")

        with self.file_path.open("r", encoding="utf-8") as file:
            har_data = json.load(file)

        log = har_data.get("log", {})
        entries = log.get("entries", [])

        parsed_requests = []

        for index, entry in enumerate(entries, start=1):

            request = entry.get("request", {})
            response = entry.get("response", {})
            content = response.get("content", {})

            parsed_url = urlparse(request.get("url", ""))

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

            parsed_requests.append({
                "id": index,

                # Request
                "method": request.get("method"),
                "url": request.get("url"),
                "scheme": parsed_url.scheme,
                "host": parsed_url.netloc,
                "path": parsed_url.path,
                "query_params": parse_qs(parsed_url.query),

                # Headers
                "headers": headers,
                "cookies": cookies,

                # Request Body
                "request_body": request_body,

                # Response
                "status_code": response.get("status"),
                "status_text": response.get("statusText"),
                "response_headers": response_headers,
                "response_size": content.get("size"),
                "mime_type": content.get("mimeType"),

                # Timing
                "response_time_ms": entry.get("time"),
                "started_date_time": entry.get("startedDateTime"),

                # Networking
                "server_ip": entry.get("serverIPAddress"),

                # Cache
                "cache": entry.get("cache")
            })

        return parsed_requests