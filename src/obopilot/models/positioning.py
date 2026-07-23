from datetime import datetime, timezone
from typing import Any, TYPE_CHECKING

from sqlmodel import JSON, Column, Field, Relationship, SQLModel

if TYPE_CHECKING:
    from obopilot.models.project import Project
    from obopilot.models.user import User


class PositioningBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    project_id: int = Field(foreign_key="projects.id", unique=True, index=True)

    status: str = Field(default="draft")
    current_step: str = Field(default="offer")

    offer: str | None = None
    uniqueness: str | None = None

    selected_options: dict | None = Field(default=None, sa_column=Column(JSON))

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


class PositioningRead(PositioningBase):
    pass


class Positioning(PositioningBase, table=True):
    __tablename__ = "positionings"

    user: "User" = Relationship(back_populates="positionings")
    project: "Project" = Relationship(back_populates="positioning")


class PositioningUpdate(SQLModel):
    status: str | None = None
    current_step: str | None = None
    offer: str | None = None
    uniqueness: str | None = None

    selected_options: dict | None = None

    target_group_options: list | None = None
    problem_options: list | None = None
    desire_options: list | None = None
    transformation_options: list | None = None
    positioning_options: list | None = None
    big_idea_options: list | None = None
    pitch_options: list | None = None
    marketing_kit: dict | None = None


class PositioningWorkflowResponse(SQLModel):
    positioning_id: int
    current_step: str
    status: str
    message: str
    coaching_hint: str | None = None
    options: list[Any] | None = None


class OfferInput(SQLModel):
    offer: str


class UniquenessInput(SQLModel):
    uniqueness: str


class WizardInput(SQLModel):
    offer: str
    uniqueness: str


class TargetGroupInput(WizardInput):
    count: int | None = 3


class OptionSelection(SQLModel):
    option_id: int


class PositioningResult(SQLModel):
    positioning_id: int
    status: str
    current_step: str
    result: dict
