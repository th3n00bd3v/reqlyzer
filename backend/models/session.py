from datetime import datetime, UTC
from typing import Optional

from pydantic import BaseModel, Field


class AnalysisSession(BaseModel):
    """
    Represents one uploaded HAR analysis session.
    """

    id: Optional[int] = None

    session_uuid: str

    filename: str

    file_size: int

    total_requests: int = 0

    overall_score: int = 0

    overall_risk: str = "Unknown"

    status: str = "Uploaded"

    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    
    completed_at: Optional[datetime] = None