from pydantic import BaseModel, Field


class SecurityFinding(BaseModel):
    """
    Represents a single security observation.
    """

    title: str

    severity: str

    description: str


class SecurityAnalysis(BaseModel):
    """
    Security analysis for one request.
    """

    https: bool = False

    authentication: str = "None"

    contains_sensitive_data: bool = False

    security_headers: list[str] = Field(default_factory=list)

    missing_headers: list[str] = Field(default_factory=list)

    findings: list[SecurityFinding] = Field(default_factory=list)

    summary: str = ""