from .api_base  import api_wrapper, APIWrapper


def me():
    return api_wrapper.api_call("/api/v1/users/me")


def register():
    email, passwd = APIWrapper.get_credentials()
    return api_wrapper.api_call("/api/v1/auth/register", "POST", {"email": email, "password": passwd})


if __name__ == "__main__":
#    register()
    print("Calling /api/v1/users/me: ")
    me()
