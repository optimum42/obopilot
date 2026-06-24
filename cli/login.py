import requests

BASE_URL = "http://127.0.0.1:8000"


def print_response(response):
    print("Status:", response.status_code)
    try:
        print("Response:", response.json())
    except requests.exceptions.JSONDecodeError:
        print("Response:", response.text)


def register(email, password):
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/register",
        json={"email": email, "password": password},
    )

    print_response(response)
    return response.json()


def login(email, password):
    response = requests.post(
        f"{BASE_URL}/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    print_response(response)

    if response.status_code == 200:
        return response.json().get("access_token")

    return None


def logout():
    response = requests.post(f"{BASE_URL}/api/v1/auth/logout")
    print_response(response)


def me(access_token=None):
    headers = {}

    if access_token:
        headers["Authorization"] = f"Bearer {access_token}"

    response = requests.get(
        f"{BASE_URL}/api/v1/auth/me",
        headers=headers,
    )

    print_response(response)


def get_credentials():
    email = input("Email: ")
    password = input("Password: ")
    return email, password


def main():
    email, password = get_credentials()
    print("Registering...")
    register(email, password)

    print("Login to your account...")
    access_token = login(email, password)

    if not access_token:
        print("Login failed.")
        return

    print("Logged in.")
    print("Calling me-route...")
    me(access_token)

    print("Log out...")
    logout()
    access_token = None

    print("Calling me-route again...")
    me(access_token)


if __name__ == "__main__":
    main()