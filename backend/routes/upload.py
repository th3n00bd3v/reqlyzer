from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile

from config import UPLOAD_DIR
from services.har_parser import HARParser
from services.request_analyzer import RequestAnalyzer
from services.security_analyzer import SecurityAnalyzer
from services.risk_scoring import RiskScorer

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_har(file: UploadFile = File(...)):
    """
    Upload a HAR file, analyze every request,
    and return the complete analysis.
    """

    # ----------------------------------------------------
    # Validate upload
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
    # Run analysis pipeline
    # ----------------------------------------------------

    try:

        parser = HARParser(destination)

        requests = parser.parse()

        request_analyzer = RequestAnalyzer()
        security_analyzer = SecurityAnalyzer()
        risk_scorer = RiskScorer()

        analyzed_requests = []

        for request in requests:

            request = request_analyzer.analyze(request)

            request = security_analyzer.analyze(request)

            request = risk_scorer.analyze(request)

            analyzed_requests.append(request.model_dump())

    except Exception as e:

        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=f"Unable to process HAR file.\n{str(e)}"
        )

    # ----------------------------------------------------
    # Optional cleanup
    # ----------------------------------------------------

    # Uncomment this if you don't want to keep uploaded HARs.
    #
    # destination.unlink(missing_ok=True)

    # ----------------------------------------------------
    # Response
    # ----------------------------------------------------

    return {
        "success": True,
        "filename": file.filename,
        "size_bytes": destination.stat().st_size,
        "total_requests": len(analyzed_requests),
        "requests": analyzed_requests
    }