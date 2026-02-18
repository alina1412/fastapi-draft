import logging

import pytest

from service.db_accessors import UserAccessor
from service.exceptions import InvalidPasswordError, InvalidUsernameError
from service.user_schema import User

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def test_db_create(session):
    user_manager = UserAccessor(session)
    user_id = await user_manager.create_user(
        User(username="test", password="123")
    )
    logger.info(user_id)
    assert user_id


@pytest.mark.parametrize(
    "username,password,expected_error,expected_match",
    [
        ("ab", "123", InvalidUsernameError, "at least 3 characters"),
        ("a" * 256, "123", InvalidUsernameError, "cannot exceed 255"),
        (
            "test@123",
            "123",
            InvalidUsernameError,
            """Username can only contain letters, numbers, and underscores""",
        ),
        ("", "123", InvalidUsernameError, "at least 3 characters"),
    ],
)
async def test_create_user_invalid_username(
    session, username, password, expected_error, expected_match
):
    user_manager = UserAccessor(session)
    with pytest.raises(expected_error, match=expected_match):
        await user_manager.create_user(
            User(username=username, password=password)
        )


@pytest.mark.parametrize(
    "username,password,expected_error,expected_match",
    [
        ("test", "12", InvalidPasswordError, "at least 3 characters"),
        ("test", "", InvalidPasswordError, "at least 3 characters"),
    ],
)
async def test_create_user_invalid_password(
    session, username, password, expected_error, expected_match
):
    user_manager = UserAccessor(session)
    with pytest.raises(expected_error, match=expected_match):
        await user_manager.create_user(
            User(username=username, password=password)
        )
