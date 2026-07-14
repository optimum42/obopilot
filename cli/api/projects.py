from .api_base import api_wrapper


def read_projects():
    return api_wrapper.api_call("/api/v1/projects", "GET")


def read_project():
    project_id = int(input("Project ID: "))
    return api_wrapper.api_call(f"/api/v1/projects/{project_id}", "GET")


def create_project():
    name = input("Project name: ")
    description = input("Project description: ")
    data = {"name": name, "description": description}
    return api_wrapper.api_call("/api/v1/projects", "POST", data)


def delete_project():
    project_id = int(input("Project ID: "))
    return api_wrapper.api_call(f"/api/v1/projects/{project_id}", "DELETE")


if __name__ == "__main__":
    read_projects()