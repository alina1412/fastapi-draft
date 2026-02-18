import pytest

from service.db_setup.models import UserModel


@pytest.fixture(scope="function")
async def user_correct(session):
    session.add(UserModel(username="test", password="123", active=1))
    await session.commit()
