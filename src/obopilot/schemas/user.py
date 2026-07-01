from sqlmodel import SQLModel


class UserCreate(SQLModel):
    email: str
    password: str


class UserRead(SQLModel):
    id: int
    email: str
    is_active: bool
    is_admin: bool


class UserUpdate(SQLModel):
    email: str | None = None
    password: str | None = None


class UserAdminUpdate(SQLModel):
    email: str | None = None
    password: str | None = None
    is_active: bool | None = None
    is_admin: bool | None = None