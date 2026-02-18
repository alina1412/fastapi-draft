import sqlalchemy as sa
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from service.db_setup.db_settings import get_session
from service.db_setup.models import UserModel

api_router = APIRouter(
    tags=["private"],
)


@api_router.get(
    "/data1",
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad request"},
        status.HTTP_422_UNPROCESSABLE_ENTITY: {"description": "Bad request"},
    },
)
async def show_data(
    # user_input: User = Depends(),
    # user_token_data=Depends(get_user_by_token)
):
    """Page"""
    return {"data": "Success"}


@api_router.get("/items")
async def get_items(session: AsyncSession = Depends(get_session)):
    result = await session.execute(sa.select(UserModel))
    items = result.scalars().all()
    return items
