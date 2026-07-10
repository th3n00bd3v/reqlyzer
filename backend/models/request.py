from typing import Any

from pydantic import BaseModel, Field

from models.analysis import RequestAnalysis
from models.metadata import Metadata
from models.risk import RiskAnalysis
from models.security import SecurityAnalysis


class AnalyzedRequest(BaseModel):
    """
    Represents one analyzed request extracted from a HAR file.
    """

    # -----------------------------------------------------
    # Basic Request Information
    # -----------------------------------------------------

    id: int

    method: str

    url: str

    scheme: str

    host: str

    path: str

    query_params: dict[str, Any] = Field(default_factory=dict)

    headers: dict[str, Any] = Field(default_factory=dict)

    cookies: list[str] = Field(default_factory=list)

    request_body: Any = None

    # -----------------------------------------------------
    # Response Information
    # -----------------------------------------------------

    status_code: int | None = None

    status_text: str | None = None

    response_headers: dict[str, Any] = Field(default_factory=dict)

    response_size: int | None = None

    mime_type: str | None = None

    response_time_ms: float | None = None

    started_date_time: str | None = None

    server_ip: str | None = None

    # -----------------------------------------------------
    # Analysis Models
    # -----------------------------------------------------

    metadata: Metadata = Field(default_factory=Metadata)

    analysis: RequestAnalysis = Field(default_factory=RequestAnalysis)

    security: SecurityAnalysis = Field(default_factory=SecurityAnalysis)

    risk: RiskAnalysis = Field(default_factory=RiskAnalysis)

    ai_summary: str = " "

    # -----------------------------------------------------
    # Helper Methods
    # -----------------------------------------------------

    def summary(self) -> str:
        """
        Returns a concise summary for debugging and logging.
        """

        return (
            f"Request #{self.id}\n"
            f"Method      : {self.method}\n"
            f"Host        : {self.host}\n"
            f"Path        : {self.path}\n"
            f"Status      : {self.status_code}\n"
            f"Response(ms): {self.response_time_ms}\n"
            f"Risk        : {self.risk.level}\n"
        )