from datetime import datetime

from sqlmodel import SQLModel


class ProjectCreate(SQLModel):
    name: str
    description: str | None = None


class ProjectUpdate(SQLModel):
    name: str | None = None
    description: str | None = None


class ProjectRead(SQLModel):
    id: int
    user_id: int
    name: str
    description: str | None
    created_at: datetime

