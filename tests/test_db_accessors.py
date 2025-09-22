import logging

import pytest

from service.db_accessors import UserAccessor

pytest_plugins = ("pytest_asyncio",)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_db_create(db):
    user_manager = UserAccessor(db)
    result = await user_manager.create_user(
        {"username": "a", "password": "123"}
    )
    logger.info(result)
