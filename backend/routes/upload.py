from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

from config import UPLOAD_DIR
from services.har_parser import HARParser
from services.request_analyzer import RequestAnalyzer
from services.security_analyzer import SecurityAnalyzer
from services.risk_scoring import RiskScorer
from services.ai.har_summarizer import HARSummarizer

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_har(file: UploadFile = File(...)):
    """
    Upload a HAR file, analyze every request,
    generate an AI executive summary,
    and return the complete analysis.
    """

    # ----------------------------------------------------
    # Validate Upload
    # ----------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    if Path(file.filename).suffix.lower() != ".har":

        raise HTTPException(
            status_code=400,
            detail="Only HAR files are supported."
        )

    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:

        shutil.copyfileobj(file.file, buffer)

    if destination.stat().st_size == 0:

        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail="Uploaded HAR file is empty."
        )

    # ----------------------------------------------------
    # Initialize Services
    # ----------------------------------------------------

    parser = HARParser(destination)

    request_analyzer = RequestAnalyzer()

    security_analyzer = SecurityAnalyzer()

    risk_scorer = RiskScorer()

    har_summarizer = HARSummarizer()

    # ----------------------------------------------------
    # Run Analysis Pipeline
    # ----------------------------------------------------

    try:

        requests = parser.parse()

        analyzed_requests = []

        for request in requests:

            request = request_analyzer.analyze(request)

            request = security_analyzer.analyze(request)

            request = risk_scorer.analyze(request)

            # AI summary will be generated on demand
            request.ai_summary = ""

            analyzed_requests.append(request)

        # ------------------------------------------------
        # Generate HAR Executive Summary (Single AI Call)
        # ------------------------------------------------

        har_summary = har_summarizer.summarize(
            analyzed_requests
        )

    except Exception as e:

        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=f"Unable to process HAR file.\n{str(e)}"
        )

    # ----------------------------------------------------
    # Optional Cleanup
    # ----------------------------------------------------

    # destination.unlink(missing_ok=True)

    # ----------------------------------------------------
    # Response
    # ----------------------------------------------------

    return {

        "success": True,

        "filename": file.filename,

        "size_bytes": destination.stat().st_size,

        "total_requests": len(analyzed_requests),

        "har_summary": har_summary,

        "requests": [
            request.model_dump()
            for request in analyzed_requests
        ]

    }