from models.request import AnalyzedRequest
from models.security import SecurityAnalysis, SecurityFinding


class SecurityAnalyzer:
    """
    Performs deterministic security analysis on a parsed request.
    """

    SENSITIVE_HEADERS = {
        "Authorization",
        "Cookie",
        "X-API-Key",
        "Api-Key",
        "X-Auth-Token",
    }

    SECURITY_HEADERS = [
        "Content-Security-Policy",
        "Strict-Transport-Security",
        "X-Frame-Options",
        "X-Content-Type-Options",
        "Referrer-Policy",
    ]

    TOKEN_PARAMETERS = {
        "token",
        "access_token",
        "apikey",
        "api_key",
        "key",
        "jwt",
    }

    def analyze(self, request: AnalyzedRequest) -> AnalyzedRequest:

        security = SecurityAnalysis()

        # --------------------------------------------------
        # HTTPS Check
        # --------------------------------------------------

        security.https = request.scheme.lower() == "https"

        if security.https:
            security.findings.append(
                SecurityFinding(
                    title="Secure Transport",
                    severity="Info",
                    description="Request is transmitted over HTTPS.",
                )
            )
        else:
            security.findings.append(
                SecurityFinding(
                    title="Insecure Transport",
                    severity="High",
                    description="Request is transmitted over HTTP.",
                )
            )

        # --------------------------------------------------
        # Authentication Detection
        # --------------------------------------------------

        if "Authorization" in request.headers:
            security.authentication = "Bearer Token"

        elif request.cookies:
            security.authentication = "Cookie"

        else:
            security.authentication = "None"

        # --------------------------------------------------
        # Sensitive Headers
        # --------------------------------------------------

        for header in self.SENSITIVE_HEADERS:

            if header in request.headers:

                security.contains_sensitive_data = True

                security.findings.append(
                    SecurityFinding(
                        title=f"Sensitive Header: {header}",
                        severity="Medium",
                        description=f"{header} is present in the request.",
                    )
                )

        # --------------------------------------------------
        # Dangerous HTTP Methods
        # --------------------------------------------------

        if request.method.upper() in {"PUT", "PATCH", "DELETE"}:

            security.findings.append(
                SecurityFinding(
                    title="State-Changing Request",
                    severity="Low",
                    description=f"{request.method} modifies server-side resources.",
                )
            )

        # --------------------------------------------------
        # File Upload Detection
        # --------------------------------------------------

        content_type = request.metadata.content_type.lower()

        if (
            "multipart/form-data" in content_type
            or "upload" in request.path.lower()
        ):

            security.findings.append(
                SecurityFinding(
                    title="File Upload Endpoint",
                    severity="Medium",
                    description="This request appears to upload files.",
                )
            )

        # --------------------------------------------------
        # Missing Cookies
        # --------------------------------------------------

        if not request.cookies:

            security.findings.append(
                SecurityFinding(
                    title="No Cookies Present",
                    severity="Low",
                    description="No cookies were included in this request.",
                )
            )

        # --------------------------------------------------
        # Large Cookie Collection
        # --------------------------------------------------

        if len(request.cookies) > 10:

            security.findings.append(
                SecurityFinding(
                    title="Large Cookie Collection",
                    severity="Low",
                    description=f"{len(request.cookies)} cookies were sent.",
                )
            )

        # --------------------------------------------------
        # API Keys / Tokens in URL
        # --------------------------------------------------

        for parameter in request.query_params.keys():

            if parameter.lower() in self.TOKEN_PARAMETERS:

                security.contains_sensitive_data = True

                security.findings.append(
                    SecurityFinding(
                        title="Sensitive Query Parameter",
                        severity="High",
                        description=f"'{parameter}' appears in the URL.",
                    )
                )

        # --------------------------------------------------
        # Missing Security Headers
        # --------------------------------------------------

        for header in self.SECURITY_HEADERS:

            if header in request.response_headers:
                security.security_headers.append(header)
            else:
                security.missing_headers.append(header)

        if security.missing_headers:

            security.findings.append(
                SecurityFinding(
                    title="Missing Security Headers",
                    severity="Medium",
                    description=(
                        f"{len(security.missing_headers)} recommended "
                        "security headers are absent."
                    ),
                )
            )

        # --------------------------------------------------
        # Server Errors
        # --------------------------------------------------

        if request.status_code and request.status_code >= 500:

            security.findings.append(
                SecurityFinding(
                    title="Server Error",
                    severity="Medium",
                    description=f"HTTP {request.status_code} returned.",
                )
            )

        # --------------------------------------------------
        # Summary
        # --------------------------------------------------

        security.summary = (
            f"{len(security.findings)} security finding(s) detected."
        )

        request.security = security

        return request