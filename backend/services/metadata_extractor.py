import json
from typing import Any


class MetadataExtractor:
    """
    Extracts security and contextual metadata from a normalized HAR request.
    """

    SENSITIVE_KEYWORDS = [
        "password",
        "passwd",
        "pwd",
        "email",
        "phone",
        "token",
        "access_token",
        "refresh_token",
        "jwt",
        "apikey",
        "api_key",
        "secret",
        "otp",
        "creditcard",
        "card",
    ]

    CATEGORY_KEYWORDS = {
        "Authentication": [
            "login",
            "logout",
            "signin",
            "signup",
            "register",
            "auth",
            "oauth",
            "token",
        ],
        "User Management": [
            "user",
            "users",
            "profile",
            "account",
        ],
        "File Upload": [
            "upload",
            "attachment",
            "image",
            "avatar",
            "media",
        ],
        "Payment": [
            "payment",
            "checkout",
            "invoice",
            "billing",
            "transaction",
        ],
        "Administration": [
            "admin",
            "dashboard",
            "manage",
        ],
    }

    def extract(self, request: dict) -> dict:
        """
        Extract metadata from a parsed HAR request.
        """

        metadata = {
            "authentication": self._detect_authentication(request),
            "request_category": self._detect_category(request),
            "uses_https": self._uses_https(request),
            "content_type": self._content_type(request),
            "contains_sensitive_data": self._contains_sensitive_data(request),
            "sensitive_fields": self._find_sensitive_fields(request),
            "has_authorization": self._has_authorization(request),
            "has_cookies": self._has_cookies(request),
            "header_count": len(request.get("headers", {})),
            "query_parameter_count": len(request.get("query_params", {})),
        }

        return metadata

    def _detect_authentication(self, request: dict) -> str:

        headers = {
            k.lower(): str(v)
            for k, v in request.get("headers", {}).items()
        }

        auth = headers.get("authorization", "")

        if auth.startswith("Bearer "):
            return "Bearer Token"

        if auth.startswith("Basic "):
            return "Basic Authentication"

        if "x-api-key" in headers:
            return "API Key"

        cookies = request.get("cookies", [])

        if cookies:
            return "Session Cookie"

        return "None"

    def _uses_https(self, request: dict) -> bool:
        return request.get("scheme", "").lower() == "https"

    def _content_type(self, request: dict):

        headers = request.get("headers", {})

        return headers.get(
            "Content-Type",
            headers.get("content-type", "Unknown")
        )

    def _has_authorization(self, request: dict) -> bool:

        headers = {
            k.lower(): str(v)
            for k, v in request.get("headers", {}).items()
        }

        return "authorization" in headers

    def _has_cookies(self, request: dict) -> bool:
        return len(request.get("cookies", [])) > 0

    def _detect_category(self, request: dict) -> str:

        path = request.get("path", "").lower()

        for category, keywords in self.CATEGORY_KEYWORDS.items():

            for keyword in keywords:

                if keyword in path:
                    return category

        return "General"

    def _contains_sensitive_data(self, request: dict) -> bool:

        return len(self._find_sensitive_fields(request)) > 0

    def _find_sensitive_fields(self, request: dict):

        found = []

        text = ""

        body = request.get("request_body")

        if body:

            if isinstance(body, dict):

                text += json.dumps(body).lower()

            else:

                text += str(body).lower()

        headers = request.get("headers", {})

        text += json.dumps(headers).lower()

        query = request.get("query_params", {})

        text += json.dumps(query).lower()

        for keyword in self.SENSITIVE_KEYWORDS:

            if keyword.lower() in text:

                found.append(keyword)

        return sorted(list(set(found)))