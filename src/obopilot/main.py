from obopilot.core.config import APP_NAME, OUTPUT_DIR, LOG_DIR, LOG_FILE
import logging
from fastapi import FastAPI
from obopilot.api.v1.router import api_router
from obopilot.db.database import create_db_and_tables

app = FastAPI(
    title="OBO Pilot API",
    version="0.1.0",
)

app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.get("/")
def root():
    return {"message": "OBO Pilot API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


def show_app():
    print(APP_NAME)
    print(OUTPUT_DIR)
    print(LOG_DIR)


def run_log():
    # Create logs directory if it does not exist
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
        ],
        force=True,
    )

    logger = logging.getLogger(__name__)

    logger.info("Application started")
    logger.info("Log file created at: %s", LOG_FILE)

    # Force writing buffered log messages
    logging.shutdown()


def main():
    run_log()
    show_app()


if __name__ == "__main__":
    main()

# Server Start
# uvicorn obopilot.main:app --reload

# oder direkt über python in der aktiven venv:
# python -m uvicorn obopilot.main:app --reload

# using fastapi
# fastapi dev main.py

# Doc by Redoc
# http://127.0.0.1:8000/redoc
