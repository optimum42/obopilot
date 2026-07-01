from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from obopilot.models.project import Project
    from obopilot.models.user import User


class Positioning(SQLModel, table=True):
    __tablename__ = "positionings"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int = Field(foreign_key="users.id", index=True)

    project_id: int = Field(
        foreign_key="projects.id",
        unique=True,
        index=True,
    )

    status: str = Field(default="draft")
    current_step: str = Field(default="offer")

    offer: str | None = None
    uniqueness: str | None = None

    selected_target_group: str | None = None
    selected_problem: str | None = None
    selected_desire: str | None = None
    selected_transformation: str | None = None
    selected_positioning: str | None = None
    selected_big_idea: str | None = None
    selected_pitch: str | None = None

    target_group_options: list | None = Field(default=None, sa_column=Column(JSON))
    problem_options: list | None = Field(default=None, sa_column=Column(JSON))
    desire_options: list | None = Field(default=None, sa_column=Column(JSON))
    transformation_options: list | None = Field(default=None, sa_column=Column(JSON))
    positioning_options: list | None = Field(default=None, sa_column=Column(JSON))
    big_idea_options: list | None = Field(default=None, sa_column=Column(JSON))
    pitch_options: list | None = Field(default=None, sa_column=Column(JSON))
    marketing_kit: dict | None = Field(default=None, sa_column=Column(JSON))

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    user: "User" = Relationship(back_populates="positionings")
    project: "Project" = Relationship(back_populates="positioning")