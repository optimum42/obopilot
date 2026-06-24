from sqlmodel import Session, select

from obopilot.db.database import engine
from obopilot.models.project import Project
from obopilot.models.user import User


def reset_database():

    with Session(engine) as session:

        projects = session.exec(
            select(Project)
        ).all()

        for project in projects:
            session.delete(project)

        users = session.exec(
            select(User)
        ).all()

        for user in users:
            session.delete(user)

        session.commit()

        print("Database reset complete.")


if __name__ == "__main__":
    reset_database()