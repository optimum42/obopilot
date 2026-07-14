from fastapi import APIRouter, Depends, status
from sqlmodel import Session, select
from fastapi import HTTPException

from obopilot.api.deps import get_current_user
from obopilot.db.session import get_session
from obopilot.models.user import User
from obopilot.models.positioning import (
    OptionSelection,
    Positioning,
    PositioningRead,
    PositioningResult,
    PositioningUpdate,
    PositioningWorkflowResponse,
    OfferInput,
    UniquenessInput,
)
from obopilot.services import positioning_service

router = APIRouter()


@router.get(
    "/positionings/",
    response_model=list[PositioningRead],
)
def read_positionings(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return positioning_service.read_positionings(
        current_user=current_user,
        session=session,
    )


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
    return positioning_service.start_positioning(
        project_id=project_id,
        current_user=current_user,
        session=session,
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
    return positioning_service.read_positioning(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    )


@router.put(
    "/positionings/{positioning_id}",
    response_model=PositioningRead,
)
def update_positioning(
    positioning_id: int,
    positioning_update: PositioningUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return positioning_service.update_positioning(
        positioning_id=positioning_id,
        positioning_update=positioning_update,
        current_user=current_user,
        session=session,
    )


@router.delete(
    "/positionings/{positioning_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_positioning(
    positioning_id: int,
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

    session.delete(positioning)
    session.commit()

    return None


@router.get(
    "/positionings/{positioning_id}/offer",
    response_model=str,
)
def read_offer(
        positioning_id: int,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
):
    return positioning_service.read_positioning(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    ).offer


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
    return positioning_service.save_offer(
        positioning_id=positioning_id,
        offer=offer_input.offer,
        current_user=current_user,
        session=session,
    )


@router.get(
    "/positionings/{positioning_id}/uniqueness",
    response_model=str,
)
def read_uniqueness(
        positioning_id: int,
        current_user: User = Depends(get_current_user),
        session: Session = Depends(get_session),
):
    return positioning_service.read_positioning(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    ).uniqueness


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
    return positioning_service.save_uniqueness(
        positioning_id=positioning_id,
        uniqueness=uniqueness_input.uniqueness,
        current_user=current_user,
        session=session,
    )


@router.get(
    "/positionings/{positioning_id}/target-group-options",
    response_model=list,
)
def read_target_group_options(
    positioning_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return positioning_service.read_positioning(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    ).target_group_options


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
    return positioning_service.select_target_group(
        positioning_id=positioning_id,
        option_id=selection.option_id,
        current_user=current_user,
        session=session,
    )


@router.get(
    "/positionings/{positioning_id}/problem-options",
    response_model=list,
)
def read_problem_options(
    positioning_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return positioning_service.read_positioning(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    ).problem_options


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
    return positioning_service.select_problem(
        positioning_id=positioning_id,
        option_id=selection.option_id,
        current_user=current_user,
        session=session,
    )


@router.get(
    "/positionings/{positioning_id}/desire-options",
    response_model=list,
)
def read_desire_options(
    positioning_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return positioning_service.read_positioning(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    ).desire_options


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
    return positioning_service.select_desire(
        positioning_id=positioning_id,
        option_id=selection.option_id,
        current_user=current_user,
        session=session,
    )


@router.get(
    "/positionings/{positioning_id}/transformation-options",
    response_model=list,
)
def read_transformation_options(
    positioning_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return positioning_service.read_positioning(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    ).transformation_options


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
    return positioning_service.select_transformation(
        positioning_id=positioning_id,
        option_id=selection.option_id,
        current_user=current_user,
        session=session,
    )


@router.get(
    "/positionings/{positioning_id}/positioning-options",
    response_model=list,
)
def read_positioning_options(
    positioning_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return positioning_service.read_positioning(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    ).positioning_options


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
    return positioning_service.select_positioning(
        positioning_id=positioning_id,
        option_id=selection.option_id,
        current_user=current_user,
        session=session,
    )


@router.get(
    "/positionings/{positioning_id}/big-idea-options",
    response_model=list,
)
def read_big_idea_options(
    positioning_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return positioning_service.read_positioning(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    ).big_idea_options


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
    return positioning_service.select_big_idea(
        positioning_id=positioning_id,
        option_id=selection.option_id,
        current_user=current_user,
        session=session,
    )


@router.get(
    "/positionings/{positioning_id}/pitch-options",
    response_model=list,
)
def read_pitch_options(
    positioning_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    return positioning_service.read_positioning(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    ).pitch_options


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
    return positioning_service.select_pitch(
        positioning_id=positioning_id,
        option_id=selection.option_id,
        current_user=current_user,
        session=session,
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
    return positioning_service.read_positioning_result(
        positioning_id=positioning_id,
        current_user=current_user,
        session=session,
    )