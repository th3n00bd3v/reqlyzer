from models.request import AnalyzedRequest


class RequestAnalyzer:
    """
    Generates a human-readable What, Who, Why, Where and How
    analysis for any backend request.
    """

    ENDPOINT_PATTERNS = {
        "login": (
            "Authentication",
            "Authenticates a user",
            "Verifies user credentials before granting access."
        ),
        "signin": (
            "Authentication",
            "Authenticates a user",
            "Verifies user credentials before granting access."
        ),
        "auth": (
            "Authentication",
            "Authenticates a user",
            "Performs user authentication."
        ),
        "logout": (
            "Authentication",
            "Logs out a user",
            "Terminates the current session."
        ),
        "register": (
            "User Management",
            "Registers a new user",
            "Creates a new user account."
        ),
        "signup": (
            "User Management",
            "Registers a new user",
            "Creates a new user account."
        ),
        "user": (
            "User Management",
            "Processes user information",
            "Retrieves or updates user information."
        ),
        "profile": (
            "User Management",
            "Processes user profile",
            "Retrieves or updates profile information."
        ),
        "search": (
            "Search",
            "Performs a search",
            "Retrieves matching information."
        ),
        "upload": (
            "File Management",
            "Uploads a file",
            "Transfers files to the backend."
        ),
        "download": (
            "File Management",
            "Downloads a file",
            "Retrieves files from the backend."
        ),
        "payment": (
            "Payment",
            "Processes a payment",
            "Transfers payment information securely."
        ),
        "checkout": (
            "Payment",
            "Processes checkout",
            "Finalizes a purchase transaction."
        ),
        "cart": (
            "E-Commerce",
            "Manages shopping cart",
            "Updates shopping cart information."
        ),
        "order": (
            "E-Commerce",
            "Processes orders",
            "Handles order information."
        ),
        "product": (
            "Product",
            "Retrieves product information",
            "Fetches product details."
        ),
        "analytics": (
            "Analytics",
            "Reports application analytics",
            "Sends application usage analytics."
        ),
        "stats": (
            "Analytics",
            "Reports application statistics",
            "Transmits statistical information."
        ),
        "report": (
            "Reporting",
            "Generates reports",
            "Produces reporting information."
        ),
        "notification": (
            "Notifications",
            "Processes notifications",
            "Delivers notification information."
        ),
        "message": (
            "Messaging",
            "Processes messages",
            "Exchanges messaging data."
        ),
        "admin": (
            "Administration",
            "Performs administrative operation",
            "Manages administrative resources."
        ),
        "config": (
            "Configuration",
            "Processes configuration",
            "Retrieves or updates configuration."
        ),
        "settings": (
            "Configuration",
            "Processes settings",
            "Retrieves or updates settings."
        ),
        "health": (
            "Monitoring",
            "Checks service health",
            "Verifies service availability."
        ),
        "status": (
            "Monitoring",
            "Checks service status",
            "Retrieves current service status."
        ),
    }

    def analyze(self, request: AnalyzedRequest) -> AnalyzedRequest:

        path = request.path.lower()
        host = request.host

        category = "General API"
        what = "Processes an API request"
        why = "Exchanges information with the backend service."

        # ---------------------------------------------
        # Detect endpoint purpose
        # ---------------------------------------------

        for keyword, values in self.ENDPOINT_PATTERNS.items():
            if keyword in path:
                category, what, why = values
                break

        # ---------------------------------------------
        # Detect client
        # ---------------------------------------------

        user_agent = request.headers.get("User-Agent", "")

        if "Firefox" in user_agent:
            client = "Firefox Browser"

        elif "Chrome" in user_agent:
            client = "Chrome Browser"

        elif "Edg" in user_agent:
            client = "Microsoft Edge"

        elif "Safari" in user_agent and "Chrome" not in user_agent:
            client = "Safari Browser"

        elif "Android" in user_agent:
            client = "Android App"

        elif "iPhone" in user_agent or "iPad" in user_agent:
            client = "iOS App"

        elif "Postman" in user_agent:
            client = "Postman"

        elif "curl" in user_agent.lower():
            client = "cURL"

        elif "python-requests" in user_agent.lower():
            client = "Python Requests"

        else:
            client = "Unknown Client"

        who = f"{client} → {host}"

        # ---------------------------------------------
        # Detect Authentication
        # ---------------------------------------------

        headers = request.headers

        if "Authorization" in headers:

            auth = headers["Authorization"]

            if auth.startswith("Bearer"):
                authentication = "Bearer Token"

            elif auth.startswith("Basic"):
                authentication = "Basic Authentication"

            else:
                authentication = "Authorization Header"

        elif "X-API-Key" in headers or "Api-Key" in headers:
            authentication = "API Key"

        elif request.cookies:
            authentication = "Cookie Authentication"

        else:
            authentication = "No Authentication"

        # ---------------------------------------------
        # Detect API Type
        # ---------------------------------------------

        if "/graphql" in path:
            api_type = "GraphQL"

        elif "/soap" in path:
            api_type = "SOAP"

        elif "/api" in path:
            api_type = "REST API"

        elif host in ("localhost", "127.0.0.1"):
            api_type = "Local Service"

        else:
            api_type = "HTTP API"

        # ---------------------------------------------
        # Where
        # ---------------------------------------------

        where = f"{host}{request.path}"

        # ---------------------------------------------
        # How
        # ---------------------------------------------

        content_type = (
            request.metadata.content_type
            or "Unknown Content-Type"
        )

        protocol = request.scheme.upper()

        how = (
            f"{protocol} • "
            f"{request.method.upper()} • "
            f"{content_type} • "
            f"{authentication}"
        )

        # ---------------------------------------------
        # Tags
        # ---------------------------------------------

        tags = [
            request.method.upper(),
            api_type,
            category,
        ]

        if authentication != "No Authentication":
            tags.append(authentication)

        if request.query_params:
            tags.append("Query Parameters")

        if request.cookies:
            tags.append("Cookies")

        if request.request_body:
            tags.append("Request Body")

        # ---------------------------------------------
        # Human-readable summary
        # ---------------------------------------------

        summary = (
            f"This request {what.lower()} through the "
            f"{category.lower()} endpoint on {host}. "
            f"It communicates using {protocol} with "
            f"the {api_type} architecture and uses "
            f"{authentication.lower()}."
        )

        # ---------------------------------------------
        # Populate analysis model
        # ---------------------------------------------

        request.analysis.what = what
        request.analysis.who = who
        request.analysis.why = why
        request.analysis.where = where
        request.analysis.how = how
        request.analysis.summary = summary
        request.analysis.detected_api = host
        request.analysis.endpoint_type = api_type
        request.analysis.endpoint_category = category
        request.analysis.tags = tags

        return request