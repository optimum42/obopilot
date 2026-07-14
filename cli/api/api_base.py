import requests
import json

BASE_URL = "http://127.0.0.1:8000"


class APIWrapper:
    def __init__(self):
        self._access_token: str = ""
        self._current_user_email = "info@hm0.de"
        self._current_user_passwd = "info123"
        self.login()

    def _print_response(self, response):
        print("Status:", response.status_code)
        try:
            print(json.dumps(
                response.json(),
                indent=4,
                sort_keys=False,
                ensure_ascii=False,
            ))
        except requests.exceptions.JSONDecodeError:
            print("Response:", response.text)

    @staticmethod
    def get_credentials():
        email = input("Email: ")
        password = input("Password: ")
        return email, password

    def get_headers(self):
        return {"Authorization": f"Bearer {self._access_token}"}

    def login(self):
        use_credentials = input("Use credentials? (y/n): ").lower() == "y"
        if use_credentials:
            self._current_user_email, self._current_user_passwd = APIWrapper.get_credentials()

        response = requests.post(
            f"{BASE_URL}/api/v1/auth/login",
            json={"email": self._current_user_email, "password": self._current_user_passwd},
        )

        self._print_response(response)

        if response.status_code == 200:
            self._access_token = response.json()["access_token"]
            return True
        return False

    def logout(self):
        self._access_token = ""

    def api_call(self, endpoint: str, method: str = "GET", data: dict = None, quiet: bool = False):
        url = f"{BASE_URL}{endpoint}"
        headers = self.get_headers()
        response = requests.request(method, url, headers=headers, json=data)
        if not quiet:
            self._print_response(response)
        return response


api_wrapper = APIWrapper()



