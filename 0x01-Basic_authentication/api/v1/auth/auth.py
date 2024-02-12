#!/usr/bin/env python3
""" Class to manage the API authentication
"""
from flask import request
from typing import List, TypeVar


class Auth():
    """authentication class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ function that determines whether a
        path needs an authentication or not
        """
        return (False)

    def authorization_header(self, request=None) -> str:
        """ gets the authentication header from the request
        """
        return (None)

    def current_user(self, request=None) -> TypeVar('User'):
        """ gets the current user from th request
        """
        return (None)
