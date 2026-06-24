from sqlmodel import SQLModel


class UserCreate(SQLModel):
    email: str
    password: str


class UserRead(SQLModel):
    id: int
    email: str
    role: str


class UserUpdate(SQLModel):
    email: str | None = None
    password: str | None = None


class UserAdminUpdate(SQLModel):
    email: str | None = None
    password: str | None = None
    role: str | None = None
