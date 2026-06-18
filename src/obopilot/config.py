# src/obopilot/config.py

from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# -------------------------------------------------------------------
# Project Paths
# -------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

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

APP_NAME = os.getenv("APP_NAME", "MyProject")

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
# Example Configuration Values
# -------------------------------------------------------------------

REQUEST_TIMEOUT = 30

MAX_RETRIES = 3