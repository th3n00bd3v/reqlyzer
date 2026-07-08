from fastapi import FastAPI

from config import APP_NAME, VERSION
from routes.upload import router as upload_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title=APP_NAME,
    version=VERSION,
    description="Reqlyzer - AI Powered Backend Request Analyzer"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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