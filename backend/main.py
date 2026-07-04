from fastapi import FastAPI

from config import APP_NAME, VERSION
from routes.upload import router as upload_router

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="Reqlyzer - AI Powered Backend Request Analyzer"
)

app.include_router(upload_router)


@app.get("/")
def root():
    return {
        "application": APP_NAME,
        "version": VERSION,
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }