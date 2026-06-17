from myproject.config import APP_NAME, OUTPUT_DIR
from myproject.config import LOG_DIR, LOG_FILE
import logging


def show_app():
    print(APP_NAME)
    print(OUTPUT_DIR)


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