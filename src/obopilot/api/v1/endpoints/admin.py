from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from obopilot.api.deps import get_current_admin_user
from obopilot.core.security import hash_password
from obopilot.db.session import get_session
from obopilot.models.project import Project, ProjectRead, ProjectUpdate
from obopilot.models.user import User, UserAdminUpdate, UserRead
from obopilot.models.positioning import Positioning, PositioningRead

router = APIRouter()


@router.get("/users", response_model=list[UserRead])
def admin_read_users(
    admin_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session),
):
    return session.exec(select(User)).all()


@router.put("/users/{user_id}", response_model=UserRead)
def admin_update_user(
    user_id: int,
    user_update: UserAdminUpdate,
    admin_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    update_data = user_update.model_dump(exclude_unset=True)

    if "email" in update_data:
        existing_user = session.exec(
            select(User).where(User.email == user_update.email)
        ).first()

        if existing_user and existing_user.id != user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A user with this email already exists.",
            )

        user.email = user_update.email

    if "password" in update_data:
        user.password_hash = hash_password(user_update.password)

    if "is_active" in update_data:
        user.is_active = user_update.is_active

    if "is_admin" in update_data:
        user.is_admin = user_update.is_admin

    user.updated_at = datetime.now(timezone.utc)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_user(
    user_id: int,
    admin_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
        )

    # delete all positionings and projects associated with this user
    positionings = session.exec(
        select(Positioning).where(Positioning.user_id == user.id)
    ).all()

    for positioning in positionings:
        session.delete(positioning)

    projects = session.exec(
        select(Project).where(Project.user_id == user.id)
    ).all()

    for project in projects:
        session.delete(project)

    session.delete(user)
    session.commit()

    return None


@router.get("/projects", response_model=list[ProjectRead])
def admin_read_projects(
    admin_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session),
):
    return session.exec(select(Project)).all()


@router.get("/projects/{project_id}", response_model=ProjectRead)
def admin_read_project(
    project_id: int,
    admin_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session),
):
    project = session.get(Project, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    return project


@router.get("/positionings", response_model=list[PositioningRead])
def admin_read_positionings(
    admin_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session),
):
    return session.exec(select(Positioning)).all()


@router.put("/projects/{project_id}", response_model=ProjectRead)
def admin_update_project(
    project_id: int,
    project_update: ProjectUpdate,
    admin_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session),
):
    project = session.get(Project, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    update_data = project_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(project, key, value)

    project.updated_at = datetime.now(timezone.utc)

    session.add(project)
    session.commit()
    session.refresh(project)

    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def admin_delete_project(
    project_id: int,
    admin_user: User = Depends(get_current_admin_user),
    session: Session = Depends(get_session),
):
    project = session.get(Project, project_id)

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found.",
        )

    # Delete all positionings associated with this project
    statement = select(Positioning).where(Positioning.project_id == project_id)
    positionings = session.exec(statement).all()

    for positioning in positionings:
        session.delete(positioning)

    session.delete(project)
    session.commit()

    return None