from typing import List, Dict


class SecurityAnalyzer:
    """
    Performs deterministic security analysis on metadata extracted
    from a parsed HAR request.
    """

    def analyze(self, request: dict) -> List[Dict]:

        findings = []

        metadata = request.get("metadata", {})

        method = request.get("method", "").upper()

        # ---------------------------------------------------
        # Rule 1: HTTP instead of HTTPS
        # ---------------------------------------------------

        if not metadata.get("uses_https", False):

            findings.append({
                "severity": "High",
                "title": "Insecure Transport",
                "description": "The request uses HTTP instead of HTTPS.",
                "recommendation": "Always use HTTPS for transmitting application data."
            })

        # ---------------------------------------------------
        # Rule 2: Sensitive Information
        # ---------------------------------------------------

        if metadata.get("contains_sensitive_data"):

            fields = ", ".join(metadata.get("sensitive_fields", []))

            findings.append({
                "severity": "Medium",
                "title": "Sensitive Data Detected",
                "description": f"Sensitive fields detected: {fields}",
                "recommendation": "Ensure sensitive information is encrypted and never logged."
            })

        # ---------------------------------------------------
        # Rule 3: Missing Authentication
        # ---------------------------------------------------

        category = metadata.get("request_category")

        if (
            category in ["User Management", "Payment", "Administration"]
            and not metadata.get("has_authorization")
        ):

            findings.append({
                "severity": "Medium",
                "title": "Missing Authorization",
                "description": "Protected endpoint without Authorization header.",
                "recommendation": "Verify that authentication is required."
            })

        # ---------------------------------------------------
        # Rule 4: Dangerous HTTP Methods
        # ---------------------------------------------------

        if method in ["PUT", "PATCH", "DELETE"]:

            findings.append({
                "severity": "Low",
                "title": "State-Changing Request",
                "description": f"{method} modifies server-side resources.",
                "recommendation": "Ensure authorization and input validation."
            })

        # ---------------------------------------------------
        # Rule 5: File Upload
        # ---------------------------------------------------

        if metadata.get("request_category") == "File Upload":

            findings.append({
                "severity": "Medium",
                "title": "File Upload Endpoint",
                "description": "File uploads should validate file type and size.",
                "recommendation": "Validate MIME types, scan uploads, and restrict executable files."
            })

        # ---------------------------------------------------
        # Rule 6: Missing Cookies
        # ---------------------------------------------------

        if not metadata.get("has_cookies"):

            findings.append({
                "severity": "Low",
                "title": "No Cookies Present",
                "description": "No cookies were included in this request.",
                "recommendation": "Verify whether session management is expected."
            })

        return findings