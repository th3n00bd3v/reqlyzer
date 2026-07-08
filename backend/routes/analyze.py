from pathlib import Path
import shutil
import tempfile

from fastapi import APIRouter, File, HTTPException, UploadFile

from parsers.har_parser import HARParser
from services.request_analyzer import RequestAnalyzer
from services.security_analyzer import SecurityAnalyzer
from services.risk_scoring import RiskScorer

router = APIRouter(prefix="/analyze", tags=["Analysis"])


@router.post("/")
async def analyze_har(file: UploadFile = File(...)):
    """
    Upload a HAR file and analyze all requests.
    """

    # ---------------------------------------------------
    # Validate file
    # ---------------------------------------------------

    if not file.filename.endswith(".har"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a valid HAR file."
        )

    # ---------------------------------------------------
    # Save uploaded file temporarily
    # ---------------------------------------------------

    temp_dir = Path(tempfile.gettempdir())
    temp_file = temp_dir / file.filename

    with temp_file.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:

        # ---------------------------------------------------
        # Parse HAR
        # ---------------------------------------------------

        parser = HARParser(temp_file)
        requests = parser.parse()

        request_analyzer = RequestAnalyzer()
        security_analyzer = SecurityAnalyzer()
        risk_scorer = RiskScorer()

        analyzed_requests = []

        # ---------------------------------------------------
        # Analyze each request
        # ---------------------------------------------------

        for request in requests:

            request = request_analyzer.analyze(request)
            request = security_analyzer.analyze(request)
            request = risk_scorer.calculate(request)

            analyzed_requests.append(request.model_dump())

        return {
            "success": True,
            "total_requests": len(analyzed_requests),
            "requests": analyzed_requests
        }

    finally:

        if temp_file.exists():
            temp_file.unlink()