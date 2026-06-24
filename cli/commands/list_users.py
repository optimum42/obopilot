from sqlmodel import Session, select

from obopilot.db.database import engine
from obopilot.models.user import User


def list_users():
    with Session(engine) as session:

        users = session.exec(
            select(User)
        ).all()

        print()
        print("Users")
        print("-" * 50)

        for user in users:
            print(
                f"{user.id:<5}"
                f"{user.role:<10}"
                f"{user.email}"
            )

        print()


if __name__ == "__main__":
    list_users()