from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from obopilot.api.deps import get_current_user
from obopilot.core.security import hash_password
from obopilot.db.session import get_session
from obopilot.models.user import User
from obopilot.models.project import Project
from obopilot.schemas.user import UserRead, UserUpdate

router = APIRouter()


@router.get("/health")
def users_health():
    return {"status": "users endpoint ready"}


@router.get("/me", response_model=UserRead)
def read_user_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.put("/me", response_model=UserRead)
def update_user_me(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    update_data = user_update.model_dump(exclude_unset=True)

    if "email" in update_data:
        statement = select(User).where(User.email == user_update.email)
        existing_user = session.exec(statement).first()

        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        current_user.email = user_update.email

    if "password" in update_data:
        current_user.password_hash = hash_password(user_update.password)

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return current_user


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_me(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    # Delete all user projects
    statement = select(Project).where(Project.user_id == current_user.id)
    projects = session.exec(statement).all()

    for project in projects:
        session.delete(project)

    # Delete the user itself
    session.delete(current_user)
    session.commit()

    return None