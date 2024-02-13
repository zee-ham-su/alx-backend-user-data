#!/usr/bin/env python3
""" Class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Determines whether a path needs authentication"""
        if path is None:
            return True
        if not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if path == excluded_path or path.startswith(excluded_path):
                return False
            if excluded_path.endswith('*') and path == excluded_path[:-1]:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ gets the authentication header from the request
        """
        if request is None:
            return None
        if "Authorization" not in request.headers:
            return None
        return request.headers["Authorization"]

    def current_user(self, request=None) -> TypeVar('User'):
        """ gets the current user from th request
        """
        return (None)
