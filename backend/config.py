from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
REPORT_DIR = BASE_DIR / "reports"
DATABASE_DIR = BASE_DIR / "database"

UPLOAD_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)
DATABASE_DIR.mkdir(exist_ok=True)

APP_NAME = "Reqlyzer"

VERSION = "0.1.0"

# ==========================================
# AI Configuration
# ==========================================

AI_PROVIDER = "ollama"
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "llama3.2:3b"
AI_TIMEOUT = 120
AI_TEMPERATURE = 0.2
AI_TOP_P = 0.9
AI_REPEAT_PENALTY = 1.1
AI_MAX_TOKENS = 180