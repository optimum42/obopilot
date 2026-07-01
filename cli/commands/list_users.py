from sqlmodel import Session, select

from obopilot.db.database import engine
from obopilot.models.user import User


def list_users():
    with Session(engine) as session:

        users = session.exec(
            select(User)
        ).all()

        print()
        print(
            f"{'Users':<10}"
            f"{'Admin':<15}"
            f"Email"
        )
        print("-" * 50)

        for user in users:
            print(
                f"{user.id:<10}"                
                f"{str(user.is_admin):<15}"
                f"{user.email:}"
            )

        print()


if __name__ == "__main__":
    list_users()