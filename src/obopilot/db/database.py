from sqlmodel import SQLModel, create_engine
from obopilot.models.user import User
from obopilot.models.project import Project
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATABASE_URL = f"sqlite:///{BASE_DIR}/data/obopilot.db"


engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)