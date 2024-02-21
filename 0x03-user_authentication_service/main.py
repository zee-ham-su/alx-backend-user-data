#!/usr/bin/env python3
"""
Main module
"""
import requests


def register_user(email: str, password: str) -> None:
    """ register_user function
    """
    endpoint = 'http://localhost:5000/users'
    data_request = {'email': email, 'password': password}
    server_response = requests.post(endpoint, data=data_request)
    print("Server response:", server_response.status_code)
    print("Response content:", server_response.content.decode())
    assert server_response.status_code == 200
    assert server_response.json() == {
        "email": email, "message": "user created"}
    print("User registered")


def log_in_wrong_password(email: str, password: str) -> None:
    """ log_in_wrong_password function
    """
    endpoint = 'http://localhost:5000/sessions'
    data_request = {'email': email, 'password': password}
    server_response = requests.post(endpoint, data=data_request)
    print("Server response:", server_response.status_code)
    assert server_response.status_code == 401
    print("Log in failed")


def profile_unlogged() -> None:
    """ profile_unlogged function
    """
    endpoint = 'http://localhost:5000/profile'
    server_response = requests.get(endpoint)
    print("Server response:", server_response.status_code)
    assert server_response.status_code == 403
    print("Profile access failed")


def log_in(email: str, password: str) -> str:
    """ log_in function
    """
    endpoint = 'http://localhost:5000/sessions'
    data_request = {'email': email, 'password': password}
    server_response = requests.post(endpoint, data=data_request)
    print("Server response:", server_response.status_code)
    assert server_response.status_code == 200
    assert server_response.json() == {"email": email, "message": "logged in"}
    print("Log in succeeded")
    return server_response.cookies['session_id']


def profile_logged(session_id: str) -> None:
    """ profile_logged function
    """
    endpoint = 'http://localhost:5000/profile'
    cookies = {'session_id': session_id}
    server_response = requests.get(endpoint, cookies=cookies)
    print("Server response:", server_response.status_code)
    assert server_response.status_code == 200
    print("Profile access succeeded")


def log_out(session_id: str) -> None:
    """ log_out function
    """
    endpoint = 'http://localhost:5000/sessions'
    cookies = {'session_id': session_id}
    server_response = requests.delete(endpoint, cookies=cookies)
    print("Server response:", server_response.status_code)
    if server_response.status_code == 302:
        assert server_response.url == 'http://localhost:5000/'
    else:
        assert server_response.status_code == 200
    print("Log out succeeded")


def reset_password_token(email: str) -> str:
    """reset_password_token function
    """
    endpoint = 'http://localhost:5000/reset_password'
    data_request = {'email': email}
    server_response = requests.post(endpoint, data=data_request)
    print("Server response:", server_response.status_code)
    if server_response.status_code == 200:
        return server_response.json()['reset_token']
    assert server_response.status_code == 401


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update_password function
    """
    endpoint = 'http://localhost:5000/reset_password'
    data_request = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password}
    server_response = requests.put(endpoint, data=data_request)
    print("Server response:", server_response.status_code)
    if server_response.status_code == 200:
        assert server_response.json() == {
            "email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
