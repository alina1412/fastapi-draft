import random
from fastapi import APIRouter, Depends, status

from sqlalchemy.ext.asyncio import AsyncSession

from service.db_setup.db_settings import get_session
from service.utils import (
    delete_some_data,
    get_some_data,
    put_some_data,
    update_some_data,
)


api_router = APIRouter(
    prefix="/v1",
    tags=["private"],
)


@api_router.put(
    "/data2",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def put_data2(add_data=None, session: AsyncSession = Depends(get_session)):
    """example with postgres sqlalchemy"""
    add_data = add_data if add_data else str(random.random())
    print(add_data)
    id_ = await put_some_data(session, {"name": add_data, "password": "bbb"})
    users = await get_some_data(session)
    print(users)
    await update_some_data(session, {"id": 1, "active": 0})
    await delete_some_data(session, {"id": 2})
    return {"user_id": id_}
