from sqlmodel import Session, select

from obopilot.db.database import engine
from obopilot.models.project import Project


def list_projects():
    with Session(engine) as session:

        projects = session.exec(
            select(Project)
        ).all()

        print()
        print("Projects")
        print("-" * 50)

        for project in projects:
            print(
                f"{project.id:<5}"
                f"{project.user_id:<5}"
                f"{project.name:<30}"
                f"{project.description}"
            )

        print()


if __name__ == "__main__":
    list_projects()