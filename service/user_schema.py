import re
from dataclasses import dataclass
from typing import Optional

from service.exceptions import InvalidPasswordError, InvalidUsernameError


@dataclass
class User:
    """Domain entity with validation"""

    username: str
    password: str
    active: bool = True
    id: Optional[int] = None

    def __post_init__(self):
        self.validate()

    def validate(self):
        """Validate domain invariants"""
        self._validate_username()
        self._validate_password()

    def _validate_username(self):
        if not self.username or len(self.username) < 3:
            raise InvalidUsernameError(
                "Username must be at least 3 characters long"
            )
        if len(self.username) > 255:
            raise InvalidUsernameError("Username cannot exceed 255 characters")
        if not re.match(r"^[a-zA-Z0-9_]+$", self.username):
            raise InvalidUsernameError(
                "Username can only contain letters, numbers, and underscores"
            )

    def _validate_password(self):
        if not self.password or len(self.password) < 3:
            raise InvalidPasswordError(
                "Password must be at least 3 characters long"
            )
        if len(self.password) > 255:
            raise InvalidPasswordError("Password cannot exceed 255 characters")

    def change_password(self, new_password: str):
        """Domain behavior with validation"""
        # You might want to add old password verification here
        self.password = new_password
        self._validate_password()
