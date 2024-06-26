#!/usr/bin/env python3
"""define a _hash_password method that takes in a password string
arguments and returns bytes"""

import bcrypt
from sqlalchemy.orm.exc import NoResultFound
from db import DB
from user import User
import bcrypt
from uuid import uuid4


def _hash_password(password: str) -> str:
    """A method that takes a password arg and return a byte"""

    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """A _generate_uuid method"""

    return str(uuid4())


class Auth:
    """Auth class"""

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """register user"""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))

    def valid_login(self, email: str, password: str) -> bool:
        """A valid_login method that takes 3 args"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """A create_session method that takes 2 args"""
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)
            return sess_id
        except NoResultFound:
            return
