from sqlalchemy import delete, or_, select, update
from sqlalchemy.dialects.postgresql import insert

from service.db_setup.models import UserModel


async def get_some_data(session):
    q = select(UserModel).where(UserModel.id == 1)
    result = await session.execute(q)
    res = result.scalars().all()
    data = [{"username": u.username, "id": u.id} for u in res]
    return data


async def put_some_data(session, data):
    q = (
        insert(UserModel)
        .values(username=data["name"], password=data["password"])
        .on_conflict_do_nothing()
    )

    result = await session.execute(q)
    if result.rowcount:
        return result.returned_defaults[0]  # id
    return None


async def update_some_data(session, data):
    stmt = (
        update(UserModel)
        .where(
            UserModel.id == data["id"],
            or_(
                UserModel.active == 1,
                UserModel.password.is_(None),
            ),
        )
        .values(**{UserModel.active.key: UserModel.active or data["active"]})
        .returning(UserModel.id)
    )
    result = list(await session.execute(stmt))
    return result


async def delete_some_data(session, data):
    stmt = delete(UserModel).where(UserModel.id == data["id"])
    result = await session.execute(stmt)
    return
