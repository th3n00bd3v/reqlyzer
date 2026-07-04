from pathlib import Path
import shutil

from fastapi import APIRouter, File, HTTPException, UploadFile
from services.metadata_extractor import MetadataExtractor
from services.security_analyzer import SecurityAnalyzer
from config import UPLOAD_DIR
from services.har_parser import HARParser

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)


@router.post("/")
async def upload_har(file: UploadFile = File(...)):
    """
    Upload and parse a HAR file.
    """

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="No file selected."
        )

    extension = Path(file.filename).suffix.lower()

    if extension != ".har":
        raise HTTPException(
            status_code=400,
            detail="Only .har files are supported."
        )

    destination = UPLOAD_DIR / file.filename

    with destination.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_size = destination.stat().st_size

    if file_size == 0:
        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail="Uploaded HAR file is empty."
        )

    try:
        parser = HARParser(destination)
        requests = parser.parse()
        
        
        extractor = MetadataExtractor()
        analyzer = SecurityAnalyzer()
    
        for request in requests:
            request["metadata"] = extractor.extract(request)

            request["security_findings"] = analyzer.analyze(request)  

    except Exception as e:
        destination.unlink(missing_ok=True)

        raise HTTPException(
            status_code=400,
            detail=f"Invalid HAR file. {str(e)}"
        )

    return {
        "success": True,
        "filename": file.filename,
        "size_bytes": file_size,
        "total_requests": len(requests),
        "preview": requests[:5]
    }