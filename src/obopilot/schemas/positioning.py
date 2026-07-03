from datetime import datetime
from typing import Any

from sqlmodel import SQLModel


class PositioningRead(SQLModel):
    id: int
    user_id: int
    project_id: int
    status: str
    current_step: str
    offer: str | None
    uniqueness: str | None
    selected_target_group: str | None
    selected_problem: str | None
    selected_desire: str | None
    selected_transformation: str | None
    selected_positioning: str | None
    selected_big_idea: str | None
    selected_pitch: str | None
    target_group_options: list | None
    problem_options: list | None
    desire_options: list | None
    transformation_options: list | None
    positioning_options: list | None
    big_idea_options: list | None
    pitch_options: list | None
    marketing_kit: dict | None
    created_at: datetime
    updated_at: datetime


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


class OptionSelection(SQLModel):
    option_id: int


class PositioningResult(SQLModel):
    positioning_id: int
    status: str
    current_step: str
    result: dict


class PositioningUpdate(SQLModel):
    status: str | None = None
    current_step: str | None = None
    offer: str | None = None
    uniqueness: str | None = None
    selected_target_group: str | None = None
    selected_problem: str | None = None
    selected_desire: str | None = None
    selected_transformation: str | None = None
    selected_positioning: str | None = None
    selected_big_idea: str | None = None
    selected_pitch: str | None = None
    target_group_options: list | None = None
    problem_options: list | None = None
    desire_options: list | None = None
    transformation_options: list | None = None
    positioning_options: list | None = None
    big_idea_options: list | None = None
    pitch_options: list | None = None
    marketing_kit: dict | None = None


