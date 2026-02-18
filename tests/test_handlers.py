import logging

from service.db_setup.models import UserModel

pytest_plugins = ("pytest_asyncio",)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


async def test_show_data_handler(client):
    url = "/data1"
    response = await client.get(url)
    assert response.status_code == 200


async def test_get_items(client, session):
    session.add(UserModel(username="test", password="123", active=1))
    await session.commit()

    response = await client.get("/items")
    assert response.status_code == 200
    assert response.json()[0]["username"] == "test"

    await session.close()
