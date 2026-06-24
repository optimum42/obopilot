from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from obopilot.api.deps import get_current_user
from obopilot.db.session import get_session
from obopilot.models.project import Project
from obopilot.models.user import User
from obopilot.schemas.project import ProjectCreate, ProjectRead, ProjectUpdate

router = APIRouter()


@router.get("/health")
def projects_health():
    return {"status": "projects endpoint ready"}


@router.post(
    "",
    response_model=ProjectRead,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project_create: ProjectCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    project = Project(
        user_id=current_user.id,
        name=project_create.name,
        description=project_create.description,
    )

    session.add(project)
    session.commit()
    session.refresh(project)

    return project


@router.get(
    "",
    response_model=list[ProjectRead],
)
def read_projects(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = select(Project).where(Project.user_id == current_user.id)
    projects = session.exec(statement).all()

    return projects


@router.get(
    "/{project_id}",
    response_model=ProjectRead,
)
def read_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
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


@router.put(
    "/{project_id}",
    response_model=ProjectRead,
)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
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

    update_data = project_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(project, key, value)

    session.add(project)
    session.commit()
    session.refresh(project)

    return project


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
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

    session.delete(project)
    session.commit()

    return None