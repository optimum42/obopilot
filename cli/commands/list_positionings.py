from sqlmodel import Session, select

from obopilot.db.database import engine
from obopilot.models.positioning import Positioning


def list_positionings():
    with Session(engine) as session:

        positionings = session.exec(
            select(Positioning)
        ).all()

        print()
        print(
            f"{'id':<10}"
            f"{'user_id':<10}"
            f"{'project_id':<15}"
            f"offer"
        )
        print("-" * 50)
        for positioning in positionings:
            print(
                f"{positioning.id:<10}"
                f"{positioning.user_id:<10}"
                f"{positioning.project_id:<15}"
                f"{positioning.offer}"
            )

        print()


if __name__ == "__main__":
    list_positionings()