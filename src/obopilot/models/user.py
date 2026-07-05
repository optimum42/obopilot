from datetime import datetime, timezone
from typing import TYPE_CHECKING
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from obopilot.models.project import Project
    from obopilot.models.positioning import Positioning


class UserBase(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)

    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)

    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class UserRead(UserBase):
    pass


class UserCreate(SQLModel):
    email: str
    password: str

    # Ein Validator, der beide Felder gleichzeitig prüft
    @field_validator("email", "password")
    @classmethod
    def check_not_empty(cls, value: str, info) -> str:
        # info.field_name enthält den Namen des Feldes (z.B. "email")
        if not value or value.strip() == "":
            raise ValueError(f"Das Feld '{info.field_name}' darf nicht leer sein.")
        return value.strip()  # Gibt den bereinigten String zurück


class User(UserBase, table=True):
    __tablename__ = "users"

    password_hash: str = Field(nullable=False)

    projects: list["Project"] = Relationship(back_populates="user")
    positionings: list["Positioning"] = Relationship(back_populates="user")


class UserUpdate(SQLModel):
    email: str | None = None
    password: str | None = None


class UserAdminUpdate(UserUpdate):
    is_active: bool | None = None
    is_admin: bool | None = None

