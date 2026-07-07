from pydantic import BaseModel, Field


class RiskAnalysis(BaseModel):
    """
    Stores the overall risk assessment generated after
    security analysis.
    """

    score: int = Field(
        default=0,
        description="Overall risk score (0-100)."
    )

    level: str = Field(
        default="Low",
        description="Overall risk level."
    )

    recommendations: list[str] = Field(
        default_factory=list,
        description="Recommended security improvements."
    )

    summary: str = Field(
        default="",
        description="Human-readable summary of the overall risk."
    )