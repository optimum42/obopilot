from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from obopilot.models.project import Project
    from obopilot.models.positioning import Positioning


class User(SQLModel, table=True):
    __tablename__ = "users"

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    password_hash: str

    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    projects: list["Project"] = Relationship(back_populates="user")
    positionings: list["Positioning"] = Relationship(back_populates="user")