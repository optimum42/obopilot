from sqlmodel import SQLModel, create_engine
from obopilot.models.user import User

DATABASE_URL = "sqlite:///data/obopilot.db"

engine = create_engine(
    DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)