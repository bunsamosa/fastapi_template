from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.import_routes import import_routes
from lib.core.logger import initialize_logger
from lib.core.middlewares import create_context

# from lib.core.cache_store import CacheStore
# from lib.core.data_store import get_connection_pool


###############################################################################
# Rest server startup hooks
###############################################################################
@asynccontextmanager
async def lifespan(fastapi: FastAPI) -> None:
    """
    Initialize modules and attach them to app
    """
    # DB connections - enable accordingly
    fastapi.cache_store = None  # CacheStore(namespace="rest_server")
    fastapi.data_store = None  # await get_connection_pool()

    # logger
    initialize_logger()
    fastapi.logger = structlog.get_logger("rest_server")

    # routers
    import_routes(fastapi)
    yield


# Create fastAPI app
app = FastAPI(lifespan=lifespan)

# Add middlewares
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# add context middleware
app.add_middleware(BaseHTTPMiddleware, dispatch=create_context)
