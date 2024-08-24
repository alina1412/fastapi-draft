from fastapi import APIRouter, Depends, status


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
def put_data2(add_data):
    """"""
    print(add_data)
    return {"data": "user_token_data"}
