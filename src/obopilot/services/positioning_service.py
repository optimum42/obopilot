import json
from datetime import datetime, timezone
from typing import Any

from fastapi import HTTPException, status
from sqlmodel import Session, select

from obopilot.models.project import Project
from obopilot.models.user import User
from obopilot.models.positioning import (
    Positioning,
    PositioningResult,
    PositioningUpdate,
    PositioningWorkflowResponse,
)
from obopilot.services import ai_service


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


def get_user_project(
    project_id: int,
    current_user: User,
    session: Session,
) -> Project:
    statement = select(Project).where(
        Project.id == project_id,
        Project.user_id == current_user.id,
    )
    project = session.exec(statement).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


def get_user_positioning(
    positioning_id: int,
    current_user: User,
    session: Session,
) -> Positioning:
    statement = select(Positioning).where(
        Positioning.id == positioning_id,
        Positioning.user_id == current_user.id,
    )
    positioning = session.exec(statement).first()

    if not positioning:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Positioning not found.",
        )

    return positioning


def ensure_step(positioning: Positioning, expected_step: str) -> None:
    return
    if positioning.current_step != expected_step:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Invalid workflow step. Expected '{expected_step}', "
                f"current step is '{positioning.current_step}'."
            ),
        )


def select_option(
    options: list[dict[str, Any]] | None,
    option_id: int,
) -> dict[str, Any]:
    if not options:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No options available for this step.",
        )

    for option in options:
        if option.get("id") == option_id:
            return option

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid option_id.",
    )


def print_json(data: dict):
    print(json.dumps(data, indent=4, ensure_ascii=False))


def save_positioning(
    positioning: Positioning,
    session: Session,
) -> Positioning:
    positioning.updated_at = now_utc()
    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    # print("=" * 80)
    # print_json(positioning.selected_options)
    # print("=" * 80)

    return positioning


def read_positionings(
    current_user: User,
    session: Session,
) -> list[Positioning]:
    statement = select(Positioning).where(
        Positioning.user_id == current_user.id
    )

    return session.exec(statement).all()


def start_positioning(
    project_id: int,
    current_user: User,
    session: Session,
) -> PositioningWorkflowResponse:
    project = get_user_project(project_id, current_user, session)

    existing = session.exec(
        select(Positioning).where(Positioning.project_id == project.id)
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Positioning already exists for this project.",
        )

    positioning = Positioning(
        user_id=current_user.id,
        project_id=project.id,
        status="draft",
        current_step="offer",
    )

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Positioning workflow started.",
        coaching_hint="Beschreibe zuerst klar, was du anbietest.",
        options=None,
    )


def read_positioning(
    positioning_id: int,
    current_user: User,
    session: Session,
) -> Positioning:
    return get_user_positioning(positioning_id, current_user, session)


def update_positioning(
    positioning_id: int,
    positioning_update: PositioningUpdate,
    current_user: User,
    session: Session,
) -> Positioning:
    positioning = get_user_positioning(positioning_id, current_user, session)

    update_data = positioning_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(positioning, key, value)

    return save_positioning(positioning, session)


def save_offer(
    positioning_id: int,
    offer: str,
    current_user: User,
    session: Session,
) -> PositioningWorkflowResponse:
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "offer")

    positioning.offer = offer
    positioning.current_step = "uniqueness"

    save_positioning(positioning, session)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Offer saved.",
        coaching_hint="Jetzt geht es darum, warum Kunden gerade dir vertrauen sollten.",
        options=None,
    )


def save_uniqueness(
    positioning_id: int,
    uniqueness: str,
    current_user: User,
    session: Session,
) -> PositioningWorkflowResponse:
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "uniqueness")

    positioning.uniqueness = uniqueness
    positioning.target_group_options = ai_service.generate_target_groups(
        offer=positioning.offer,
        uniqueness=positioning.uniqueness,
    )
    positioning.current_step = "target_group"

    save_positioning(positioning, session)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Target group options generated.",
        coaching_hint="Unterschiedliche Zielgruppen kaufen dasselbe Angebot aus unterschiedlichen Gründen.",
        options=positioning.target_group_options,
    )


def select_target_group(
    positioning_id: int,
    option_id: int,
    current_user: User,
    session: Session,
) -> PositioningWorkflowResponse:
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "target_group")

    selected_options = dict(positioning.selected_options) if positioning.selected_options else {}
    selected_options["selected_target_group"] = select_option(
        positioning.target_group_options,
        option_id,
    )
    positioning.selected_options = selected_options
    print(positioning.selected_options)

    positioning.problem_options = ai_service.generate_problems(
        offer=positioning.offer,
        uniqueness=positioning.uniqueness,
        selected_target_group=positioning.selected_options["selected_target_group"],
    )

    positioning.current_step = "problem"
    save_positioning(positioning, session)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Problem options generated.",
        coaching_hint="Erfolgreiches Marketing beginnt mit dem relevantesten Kundenproblem.",
        options=positioning.problem_options,
    )


def select_problem(
    positioning_id: int,
    option_id: int,
    current_user: User,
    session: Session,
) -> PositioningWorkflowResponse:
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "problem")

    selected_options = dict(positioning.selected_options) if positioning.selected_options else {}
    selected_options["selected_problem"] = select_option(
        positioning.problem_options,
        option_id,
    )
    positioning.selected_options = selected_options

    positioning.desire_options = ai_service.generate_desires(
        selected_target_group=positioning.selected_options["selected_target_group"],
        selected_problem=positioning.selected_options["selected_problem"],
    )

    positioning.current_step = "desire"
    save_positioning(positioning, session)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Desire options generated.",
        coaching_hint="Hinter jedem Problem steht ein gewünschter Zielzustand.",
        options=positioning.desire_options,
    )


def select_desire(
    positioning_id: int,
    option_id: int,
    current_user: User,
    session: Session,
) -> PositioningWorkflowResponse:
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "desire")

    selected_options = dict(positioning.selected_options) if positioning.selected_options else {}
    selected_options["selected_desire"] = select_option(
        positioning.desire_options,
        option_id,
    )
    positioning.selected_options = selected_options

    positioning.transformation_options = ai_service.generate_transformations(
        selected_target_group=positioning.selected_options["selected_target_group"],
        selected_problem=positioning.selected_options["selected_problem"],
        selected_desire=positioning.selected_options["selected_desire"],
    )

    positioning.current_step = "transformation"
    save_positioning(positioning, session)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Transformation options generated.",
        coaching_hint="Eine starke Positionierung beschreibt den Weg vom Problem zum Ergebnis.",
        options=positioning.transformation_options,
    )


def select_transformation(
    positioning_id: int,
    option_id: int,
    current_user: User,
    session: Session,
) -> PositioningWorkflowResponse:
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "transformation")

    selected_options = dict(positioning.selected_options) if positioning.selected_options else {}
    selected_options["selected_transformation"] = select_option(
        positioning.transformation_options,
        option_id,
    )
    positioning.selected_options = selected_options

    positioning.positioning_options = ai_service.generate_positioning_options(
        offer=positioning.offer,
        uniqueness=positioning.uniqueness,
        selected_target_group=positioning.selected_options["selected_target_group"],
        selected_problem=positioning.selected_options["selected_problem"],
        selected_desire=positioning.selected_options["selected_desire"],
        selected_transformation=positioning.selected_options["selected_transformation"],
    )

    positioning.current_step = "positioning"
    save_positioning(positioning, session)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Positioning options generated.",
        coaching_hint="Die Positionierung verbindet Zielgruppe, Problem, Angebot und Ergebnis.",
        options=positioning.positioning_options,
    )


def select_positioning(
    positioning_id: int,
    option_id: int,
    current_user: User,
    session: Session,
) -> PositioningWorkflowResponse:
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "positioning")

    selected_options = dict(positioning.selected_options) if positioning.selected_options else {}
    selected_options["selected_positioning"] = select_option(
        positioning.positioning_options,
        option_id,
    )
    positioning.selected_options = selected_options

    positioning.big_idea_options = ai_service.generate_big_ideas(
        selected_positioning=positioning.selected_options["selected_positioning"],
    )

    positioning.current_step = "big_idea"
    save_positioning(positioning, session)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Big Marketing Idea options generated.",
        coaching_hint="Die Big Marketing Idea macht die Positionierung merkfähig.",
        options=positioning.big_idea_options,
    )


def select_big_idea(
    positioning_id: int,
    option_id: int,
    current_user: User,
    session: Session,
) -> PositioningWorkflowResponse:
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "big_idea")

    selected_options = dict(positioning.selected_options) if positioning.selected_options else {}
    selected_options["selected_big_idea"] = select_option(
        positioning.big_idea_options,
        option_id,
    )
    positioning.selected_options = selected_options

    positioning.pitch_options = ai_service.generate_pitch_options(
        selected_target_group=positioning.selected_options["selected_target_group"],
        selected_problem=positioning.selected_options["selected_problem"],
        selected_desire=positioning.selected_options["selected_desire"],
        selected_positioning=positioning.selected_options["selected_positioning"],
        selected_big_idea=positioning.selected_options["selected_big_idea"],
    )

    positioning.current_step = "pitch"
    save_positioning(positioning, session)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Pitch options generated.",
        coaching_hint="Ein guter Pitch macht sofort klar, für wen du welches Problem löst.",
        options=positioning.pitch_options,
    )


def select_pitch(
    positioning_id: int,
    option_id: int,
    current_user: User,
    session: Session,
) -> PositioningWorkflowResponse:
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "pitch")

    selected_options = dict(positioning.selected_options) if positioning.selected_options else {}
    selected_options["selected_pitch"] = select_option(
        positioning.pitch_options,
        option_id,
    )
    positioning.selected_options = selected_options

    positioning.marketing_kit = ai_service.generate_marketing_kit(
        offer=positioning.offer,
        uniqueness=positioning.uniqueness,
        selected_target_group=positioning.selected_options["selected_target_group"],
        selected_problem=positioning.selected_options["selected_problem"],
        selected_desire=positioning.selected_options["selected_desire"],
        selected_transformation=positioning.selected_options["selected_transformation"],
        selected_positioning=positioning.selected_options["selected_positioning"],
        selected_big_idea=positioning.selected_options["selected_big_idea"],
        selected_pitch=positioning.selected_options["selected_pitch"],
    )

    positioning.current_step = "finished"
    positioning.status = "completed"

    save_positioning(positioning, session)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Positioning workflow finished.",
        coaching_hint="Dein Marketing-Kit wurde erstellt.",
        options=None,
    )


def read_positioning_result(
    positioning_id: int,
    current_user: User,
    session: Session,
) -> PositioningResult:
    positioning = get_user_positioning(positioning_id, current_user, session)

    if positioning.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Positioning is not completed yet.",
        )

    return PositioningResult(
        positioning_id=positioning.id,
        status=positioning.status,
        current_step=positioning.current_step,
        result=positioning.marketing_kit or {},
    )
