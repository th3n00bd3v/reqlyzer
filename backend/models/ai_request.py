from pydantic import BaseModel


class AIRequest(BaseModel):
    """
    Request sent from the frontend when the user
    wants an AI explanation for a single request.
    """

    request: dict