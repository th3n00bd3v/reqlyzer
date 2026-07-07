from pydantic import BaseModel, Field

class RequestAnalysis(BaseModel):
    """
    Human-readable explanation of the request.
    """

    what: str = ""
    who: str = ""
    why: str = ""
    where: str = ""
    how: str = ""
    summary: str = ""
    detected_api: str = ""
    endpoint_type: str = ""
    endpoint_category: str = ""

    tags: list[str] = Field(default_factory=list)