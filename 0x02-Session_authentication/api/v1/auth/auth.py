#!/usr/bin/env python3
""" Class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar
import os


class Auth():
    """authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines whether a path needs authentication"""
        if path is None:
            return True

        if excluded_paths is None or excluded_paths == []:
            return True

        if path in excluded_paths:
            return False

        for excluded_path in excluded_paths:
            if excluded_path.startswith(path):
                return False
            elif path.startswith(excluded_path):
                return False
            elif excluded_path[-1] == "*":
                if path.startswith(excluded_path[:-1]):
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """ gets the authentication header from the request
        """
        if request is None:
            return None
        header_key = request.headers.get('Authorization')

        if header_key is None:
            return None

        return header_key

    def current_user(self, request=None) -> TypeVar('User'):
        """ gets the current user from th request
        """
        return (None)

    def session_cookie(self, request=None):
        """ returns the session cookie from the request
        """
        if request is None:
            return None

        return request.cookies.get(
            os.environ.get(
                'SESSION_NAME',
                '_my_session_id'))
