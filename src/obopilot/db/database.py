from sqlmodel import SQLModel, create_engine

from obopilot.models.positioning import Positioning  # noqa: F401
from obopilot.models.project import Project  # noqa: F401
from obopilot.models.user import User  # noqa: F401

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]
DATABASE_URL = f"sqlite:///{BASE_DIR}/data/obopilot.db"


engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
# usage of alembic doesn't need create_db_and_tables anymore
#    SQLModel.metadata.create_all(engine)
    pass
