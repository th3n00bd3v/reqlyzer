from fastapi import APIRouter

from models.ai_request import AIRequest
from models.request import AnalyzedRequest
from services.ai.ai_analyzer import AIAnalyzer

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.post("/request")
async def analyze_request(
    payload: AIRequest
):

    request = AnalyzedRequest.model_validate(
        payload.request
    )

    analyzer = AIAnalyzer()

    request = analyzer.analyze(request)

    return {

        "success": True,

        "summary": request.ai_summary

    }