import logging

import pytest
import pytest_asyncio

pytest_plugins = ("pytest_asyncio",)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

pytestmark = pytest.mark.asyncio


async def test_show_data_handler(client):
    url = "v1/data1"
    response = client.get(url)
    assert response.status_code == 200
