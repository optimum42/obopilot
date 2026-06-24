import sys

from commands.seed_db import seed_database
from commands.make_admin import make_admin
from commands.make_user import make_user
from commands.list_users import list_users
from commands.list_projects import list_projects
from commands.reset_db import reset_database


def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python cli/manage.py seed")
        print("  python cli/manage.py make-admin EMAIL")
        print("  python cli/manage.py make-user EMAIL")
        print("  python cli/manage.py list-users")
        print("  python cli/manage.py list-projects")
        print("  python cli/manage.py reset-db")
        return

    command = sys.argv[1]

    if command == "seed":
        seed_database()

    elif command == "make-admin":
        if len(sys.argv) < 3:
            print("Email required.")
            return

        make_admin(sys.argv[2])

    elif command == "make-user":
        if len(sys.argv) < 3:
            print("Email required.")
            return

        make_user(sys.argv[2])

    elif command == "list-users":
        list_users()

    elif command == "list-projects":
        list_projects()

    elif command == "reset-db":
        reset_database()

    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()