from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from obopilot.core.config import ACCESS_TOKEN_EXPIRE_DELTA
from obopilot.core.security import (
    create_access_token,
    hash_password,
    verify_password,
)
from obopilot.db.session import get_session
from obopilot.models.user import User
from obopilot.schemas.token import Token
from obopilot.schemas.user import UserCreate, UserRead
from obopilot.api.deps import get_current_user

router = APIRouter()


@router.get("/health")
def auth_health():
    return {"status": "auth endpoint ready"}


@router.post(
    "/register",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
def register_user(
    user_create: UserCreate,
    session: Session = Depends(get_session),
):
    statement = select(User).where(User.email == user_create.email)
    existing_user = session.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    user = User(
        email=user_create.email,
        password_hash=hash_password(user_create.password),
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


@router.post("/login", response_model=Token)
def login_user(
    user_create: UserCreate,
    session: Session = Depends(get_session),
):
    statement = select(User).where(User.email == user_create.email)
    user = session.exec(statement).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    if not verify_password(user_create.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
        )

    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=ACCESS_TOKEN_EXPIRE_DELTA,
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@router.post("/logout")
def logout_user():
    return {
        "message": "Logged out. Please remove the access token on the client side."
    }


@router.get("/me", response_model=UserRead)
def read_current_user(
    current_user: User = Depends(get_current_user),
):
    return current_user