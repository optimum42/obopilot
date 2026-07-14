from .api_base import api_wrapper


def read_all_positionings():
    response = api_wrapper.api_call("/api/v1/admin/positionings", "GET", quiet=True)

    for positioning in response.json():
        print(f"id: {positioning['id']}: {positioning['user_id']}")
    return response


def read_positionings():
    response = api_wrapper.api_call("/api/v1/positionings", "GET", quiet=True)

    for positioning in response.json():
        print(f"id: {positioning['id']}: {positioning['user_id']}")
    return response


def read_positioning():
    positioning_id = int(input("Positioning ID: "))
    return api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}", "GET")


def create_positioning():
    project_id = int(input("Project ID: "))
    return api_wrapper.api_call(f"/api/v1/projects/{project_id}/positioning", "POST")


def update_positioning():
    positioning_id = int(input("Positioning ID: "))
    data = {"status": "draft", "current_step": input("Current step: ")}
    return api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}", "PUT", data)


def delete_positioning():
    positioning_id = int(input("Positioning ID: "))
    return api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}", "DELETE")


def workflow_positioning():
    positioning_id = int(input("Positioning ID: "))

    data = {"offer": input("Offer: ")}
    api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}/offer", "POST", data)

    data = {"uniqueness": input("Uniqueness: ")}
    api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}/uniqueness", "POST", data)

    data = {"option_id": int(input("Auswahl: "))}
    api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}/target-group", "POST", data)

    data = {"option_id": int(input("Auswahl: "))}
    api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}/problem", "POST", data)

    data = {"option_id": int(input("Auswahl: "))}
    api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}/desire", "POST", data)

    data = {"option_id": int(input("Auswahl: "))}
    api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}/transformation", "POST", data)

    data = {"option_id": int(input("Auswahl: "))}
    api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}/positioning", "POST", data)

    data = {"option_id": int(input("Auswahl: "))}
    api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}/big-idea", "POST", data)

    data = {"option_id": int(input("Auswahl: "))}
    api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}/pitch", "POST", data)

    api_wrapper.api_call(f"/api/v1/positionings/{positioning_id}/result", "GET")


if __name__ == "__main__":
    read_positionings()
#    read_positioning()
#    delete_positioning()
#    create_positioning()
#    workflow_positioning()

