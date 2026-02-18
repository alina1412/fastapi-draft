from fastapi import FastAPI, HTTPException, status

from service.exceptions import UserNotFound


class UserNotFoundHttpException(HTTPException):
    def __init__(self, user_id: int):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(UserNotFound)
    async def user_not_found_handler(request, exc):
        raise HTTPException(status_code=404, detail=str(exc))

    return app
