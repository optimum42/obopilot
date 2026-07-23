# src/obopilot/config.py

from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# -------------------------------------------------------------------
# Application
# -------------------------------------------------------------------
APP_NAME = "OBO-Pilot API"
APP_VERSION = "0.4.1"

# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[3]

SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
OUTPUT_DIR = PROJECT_ROOT / "output"
LOG_DIR = PROJECT_ROOT / "logs"

# Create important directories automatically
DATA_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# -------------------------------------------------------------------
# Environment Variables
# -------------------------------------------------------------------

API_KEY = os.getenv("API_KEY", "")
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    "https://api.example.com"
)

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# -------------------------------------------------------------------
# Logging
# -------------------------------------------------------------------

LOG_FILE = LOG_DIR / "app.log"

# -------------------------------------------------------------------
# JWT Auth
# -------------------------------------------------------------------

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise ValueError("SECRET_KEY not configured")

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 180

ACCESS_TOKEN_EXPIRE_DELTA = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)