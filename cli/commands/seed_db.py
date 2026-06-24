from sqlmodel import Session, select

from obopilot.core.security import hash_password
from obopilot.db.database import engine
from obopilot.models.project import Project
from obopilot.models.user import User


def clear_database(session: Session) -> None:
    print("Deleting existing data...")

    projects = session.exec(select(Project)).all()
    for project in projects:
        session.delete(project)

    users = session.exec(select(User)).all()
    for user in users:
        session.delete(user)

    session.commit()


def create_demo_user(
    session: Session,
    email: str,
    password: str,
    role: str = "user",
) -> User:
    user = User(
        email=email,
        password_hash=hash_password(password),
        role=role,
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user


def create_demo_projects(
    session: Session,
    user: User,
) -> None:
    projects = [
        Project(
            user_id=user.id,
            name=f"{user.email} Project 1",
            description="Demo project 1",
        ),
        Project(
            user_id=user.id,
            name=f"{user.email} Project 2",
            description="Demo project 2",
        ),
    ]

    for project in projects:
        session.add(project)

    session.commit()


def seed_database():
    with Session(engine) as session:

        clear_database(session)

        print("Creating demo users...")

        users = [
            create_demo_user(
                session,
                "user1@example.com",
                "secret123",
            ),
            create_demo_user(
                session,
                "user2@example.com",
                "secret123",
            ),
            create_demo_user(
                session,
                "user3@example.com",
                "secret123",
            ),
        ]

        print("Creating projects...")

        for user in users:
            create_demo_projects(
                session=session,
                user=user,
            )

        print("Creating admin user...")

        create_demo_user(
            session,
            "admin@example.com",
            "admin123",
            role="admin",
        )

        print()
        print("Database seeded successfully.")
        print()
        print("Users:")
        print("  user1@example.com / secret123")
        print("  user2@example.com / secret123")
        print("  user3@example.com / secret123")
        print()
        print("Admin:")
        print("  admin@example.com / admin123")


if __name__ == "__main__":
    seed_database()