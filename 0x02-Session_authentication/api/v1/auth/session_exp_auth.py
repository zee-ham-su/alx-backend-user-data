#!/usr/bin/env python3
""" session expiration class module
"""

from datetime import datetime, timedelta
from os import getenv
from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """SESSION EXPIRATION CLASS
    """

    def __init__(self) -> None:
        self.session_duration = int(getenv('SESSION_DURATION', 0))

    def create_session(self, user_id: str = None) -> str:
        """Create a session for a user_id
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Return a User ID based on a Session ID
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_info = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_info['user_id']

        created_at = session_info.get('created_at')
        if created_at is None:
            return None

        expire_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expire_time:
            return None

        return session_info['user_id']
