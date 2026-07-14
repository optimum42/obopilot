from .api_base import api_wrapper


def read_users():
    return api_wrapper.api_call("/api/v1/admin/users", "GET")


def update_user():
    user_id = int(input("User ID: "))
    is_admin = input("Is admin? (y/n): ") == "y"
    data = {"is_admin": is_admin}
    return api_wrapper.api_call(f"/api/v1/admin/users/{user_id}", "PUT", data)


def delete_user():
    user_id = int(input("User ID: "))
    if input("Are you sure? (y/n): ") == "y":
        return api_wrapper.api_call(f"/api/v1/admin/users/{user_id}", "DELETE")


def read_positionings():
    return api_wrapper.api_call("/api/v1/admin/positionings")


if __name__ == "__main__":
#    read_users()
#    update_user()
#    delete_user()
    read_positionings()
