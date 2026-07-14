from .auth import register, me
from .admin import read_users, update_user, delete_user
from .projects import read_projects, read_project, create_project, delete_project
from .positionings import *


def show_menu_and_get_input():
    print("Menu:")
    for key, value in menu.items():
        print(f"{key}. {value[1]}")

    while True:
        try:
            choice = int(input('Your choice (0 to exit): '))
            if choice in menu:
                return menu[choice][0]
        except ValueError as e:
            pass
        print("Try again...")


menu = {
    1: (register, "Register user"),
    2: (me, "Me"),
    3: (read_users, "Read users"),
    4: (update_user, "Update user"),
    5: (delete_user, "Delete user"),
    6: (read_projects, "My projects"),
    7: (read_project, "Project details"),
    8: (create_project, "New project"),
    9: (delete_project, "Delete project"),
    10: (read_positionings, "My positionings"),
    11: (read_all_positionings, "All positionings"),
    12: (read_positioning, "Positioning details"),
    13: (create_positioning, "New positioning"),
    14: (delete_positioning, "Delete positioning"),
    15: (update_positioning, "Update positioning"),
    16: (workflow_positioning, "Workflow positioning"),
    0: (quit, "Exit")
}


def main():
    while True:
        choice_func = show_menu_and_get_input()
        choice_func()


if __name__ == "__main__":
    main()