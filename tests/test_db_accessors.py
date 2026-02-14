import logging

from service.db_accessors import UserAccessor

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def test_db_create(session):
    user_manager = UserAccessor(session)
    result = await user_manager.create_user(
        {"username": "a", "password": "123"}
    )
    logger.info(result)
