from datetime import datetime, timezone
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from obopilot.api.deps import get_current_user
from obopilot.db.session import get_session
from obopilot.models.positioning import Positioning
from obopilot.models.project import Project
from obopilot.models.user import User
from obopilot.schemas.positioning import (
    OfferInput,
    OptionSelection,
    PositioningRead,
    PositioningUpdate,
    PositioningResult,
    PositioningWorkflowResponse,
    UniquenessInput,
)

router = APIRouter()


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
    if positioning.current_step != expected_step:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid workflow step. Expected '{expected_step}', current step is '{positioning.current_step}'.",
        )


def select_option(options: list[dict[str, Any]] | None, option_id: int) -> str:
    if not options:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No options available for this step.",
        )

    for option in options:
        if option.get("id") == option_id:
            return option.get("name") or option.get("text")

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid option_id.",
    )


def demo_options(prefix: str, count: int = 10) -> list[dict[str, Any]]:
    return [
        {
            "id": index,
            "name": f"{prefix} {index}",
            "description": f"Demo-Beschreibung für {prefix} {index}",
            "reason": "Demo-Begründung für diese Option.",
            "score": 100 - index,
        }
        for index in range(1, count + 1)
    ]


@router.post(
    "/projects/{project_id}/positioning",
    response_model=PositioningWorkflowResponse,
    status_code=status.HTTP_201_CREATED,
)
def start_positioning(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
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


@router.get(
    "/positionings/{positioning_id}",
    response_model=PositioningRead,
)
def read_positioning(
    positioning_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return get_user_positioning(positioning_id, current_user, session)


@router.put(
    "/positionings/{positioning_id}",
    response_model=PositioningUpdate,
)
def update_positioning(
    positioning_id: int,
    positioning_update: PositioningUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
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

    update_data = positioning_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(positioning, key, value)

    positioning.updated_at = datetime.now(timezone.utc)

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return positioning


@router.post(
    "/positionings/{positioning_id}/offer",
    response_model=PositioningWorkflowResponse,
)
def save_offer(
    positioning_id: int,
    offer_input: OfferInput,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "offer")

    positioning.offer = offer_input.offer
    positioning.current_step = "uniqueness"
    positioning.updated_at = now_utc()

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Offer saved.",
        coaching_hint="Jetzt geht es darum, warum Kunden gerade dir vertrauen sollten.",
        options=None,
    )


@router.post(
    "/positionings/{positioning_id}/uniqueness",
    response_model=PositioningWorkflowResponse,
)
def save_uniqueness(
    positioning_id: int,
    uniqueness_input: UniquenessInput,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "uniqueness")

    positioning.uniqueness = uniqueness_input.uniqueness
    positioning.target_group_options = demo_options("Zielgruppe")
    positioning.current_step = "target_group"
    positioning.updated_at = now_utc()

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Target group options generated.",
        coaching_hint="Unterschiedliche Zielgruppen kaufen dasselbe Angebot aus unterschiedlichen Gründen.",
        options=positioning.target_group_options,
    )


@router.post(
    "/positionings/{positioning_id}/target-group",
    response_model=PositioningWorkflowResponse,
)
def select_target_group(
    positioning_id: int,
    selection: OptionSelection,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "target_group")

    positioning.selected_target_group = select_option(
        positioning.target_group_options,
        selection.option_id,
    )
    positioning.problem_options = demo_options("Problem")
    positioning.current_step = "problem"
    positioning.updated_at = now_utc()

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Problem options generated.",
        coaching_hint="Erfolgreiches Marketing beginnt mit dem relevantesten Kundenproblem.",
        options=positioning.problem_options,
    )


@router.post(
    "/positionings/{positioning_id}/problem",
    response_model=PositioningWorkflowResponse,
)
def select_problem(
    positioning_id: int,
    selection: OptionSelection,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "problem")

    positioning.selected_problem = select_option(positioning.problem_options, selection.option_id)
    positioning.desire_options = demo_options("Wunsch")
    positioning.current_step = "desire"
    positioning.updated_at = now_utc()

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Desire options generated.",
        coaching_hint="Hinter jedem Problem steht ein gewünschter Zielzustand.",
        options=positioning.desire_options,
    )


@router.post(
    "/positionings/{positioning_id}/desire",
    response_model=PositioningWorkflowResponse,
)
def select_desire(
    positioning_id: int,
    selection: OptionSelection,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "desire")

    positioning.selected_desire = select_option(positioning.desire_options, selection.option_id)
    positioning.transformation_options = demo_options("Transformation")
    positioning.current_step = "transformation"
    positioning.updated_at = now_utc()

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Transformation options generated.",
        coaching_hint="Eine starke Positionierung beschreibt den Weg vom Problem zum Ergebnis.",
        options=positioning.transformation_options,
    )


@router.post(
    "/positionings/{positioning_id}/transformation",
    response_model=PositioningWorkflowResponse,
)
def select_transformation(
    positioning_id: int,
    selection: OptionSelection,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "transformation")

    positioning.selected_transformation = select_option(
        positioning.transformation_options,
        selection.option_id,
    )
    positioning.positioning_options = demo_options("Positionierung", count=3)
    positioning.current_step = "positioning"
    positioning.updated_at = now_utc()

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Positioning options generated.",
        coaching_hint="Die Positionierung verbindet Zielgruppe, Problem, Angebot und Ergebnis.",
        options=positioning.positioning_options,
    )


@router.post(
    "/positionings/{positioning_id}/positioning",
    response_model=PositioningWorkflowResponse,
)
def select_positioning(
    positioning_id: int,
    selection: OptionSelection,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "positioning")

    positioning.selected_positioning = select_option(
        positioning.positioning_options,
        selection.option_id,
    )
    positioning.big_idea_options = demo_options("Big Marketing Idea", count=3)
    positioning.current_step = "big_idea"
    positioning.updated_at = now_utc()

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Big Marketing Idea options generated.",
        coaching_hint="Die Big Marketing Idea macht die Positionierung merkfähig.",
        options=positioning.big_idea_options,
    )


@router.post(
    "/positionings/{positioning_id}/big-idea",
    response_model=PositioningWorkflowResponse,
)
def select_big_idea(
    positioning_id: int,
    selection: OptionSelection,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "big_idea")

    positioning.selected_big_idea = select_option(
        positioning.big_idea_options,
        selection.option_id,
    )
    positioning.pitch_options = demo_options("Pitch", count=3)
    positioning.current_step = "pitch"
    positioning.updated_at = now_utc()

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Pitch options generated.",
        coaching_hint="Ein guter Pitch macht sofort klar, für wen du welches Problem löst.",
        options=positioning.pitch_options,
    )


@router.post(
    "/positionings/{positioning_id}/pitch",
    response_model=PositioningWorkflowResponse,
)
def select_pitch(
    positioning_id: int,
    selection: OptionSelection,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    positioning = get_user_positioning(positioning_id, current_user, session)
    ensure_step(positioning, "pitch")

    positioning.selected_pitch = select_option(positioning.pitch_options, selection.option_id)

    positioning.marketing_kit = {
        "offer": positioning.offer,
        "uniqueness": positioning.uniqueness,
        "target_group": positioning.selected_target_group,
        "problem": positioning.selected_problem,
        "desire": positioning.selected_desire,
        "transformation": positioning.selected_transformation,
        "positioning": positioning.selected_positioning,
        "big_marketing_idea": positioning.selected_big_idea,
        "elevator_pitch": positioning.selected_pitch,
    }

    positioning.current_step = "finished"
    positioning.status = "completed"
    positioning.updated_at = now_utc()

    session.add(positioning)
    session.commit()
    session.refresh(positioning)

    return PositioningWorkflowResponse(
        positioning_id=positioning.id,
        current_step=positioning.current_step,
        status=positioning.status,
        message="Positioning workflow finished.",
        coaching_hint="Dein Marketing-Kit wurde erstellt.",
        options=None,
    )


@router.get(
    "/positionings/{positioning_id}/result",
    response_model=PositioningResult,
)
def read_positioning_result(
    positioning_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
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