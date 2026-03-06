from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from service.config import logger
from service.db_setup.db_settings import db_connector
from service.endpoints.data_handlers import api_router as data_routes
from service.endpoints.put_handlers import api_router as put_routes
from service.endpoints.update_handlers import api_router as upd_routes
from service.http_exceptions import add_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up...")
    yield
    logger.warning("Shutting down...")
    await db_connector.dispose_engine()


app = FastAPI(
    lifespan=lifespan,
    docs_url="/docs",
)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="Educational FastApi REST API",
        version="3.1.0",
        routes=app.routes,
    )

    # ensure components exist (some versions of fastapi may not include it by default)
    if (
        "components" not in openapi_schema
        or openapi_schema["components"] is None
    ):
        openapi_schema["components"] = {}

    # TODO: adjust security schemes to your needs
    openapi_schema["components"].setdefault("securitySchemes", {})
    openapi_schema["components"]["securitySchemes"].update(
        {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            },
            "apiKey": {
                "type": "apiKey",
                "name": "client_secret",
                "in": "header",
                "scheme": "apiKey",
            },
        }
    )
    openapi_schema["security"] = [
        {"bearerAuth": ["read", "write"], "apiKey": ["read", "write"]}
    ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app = add_exception_handlers(app)

app.include_router(put_routes)
app.include_router(upd_routes)
app.include_router(data_routes)
app.openapi = custom_openapi

if __name__ == "__main__":
    uvicorn.run("service.__main__:app", host="0.0.0.0", port=8000, reload=True)
