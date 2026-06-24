from sqlmodel import Session, select

from obopilot.db.database import engine
from obopilot.models.user import User


def make_user(email: str):

    with Session(engine) as session:

        user = session.exec(
            select(User).where(
                User.email == email
            )
        ).first()

        if not user:
            print("User not found.")
            return

        user.role = "user"

        session.add(user)
        session.commit()

        print(
            f"{user.email} promoted to admin."
        )