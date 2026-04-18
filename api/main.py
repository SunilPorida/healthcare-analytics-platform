"""FastAPI application factory and ASGI entrypoint."""

from __future__ import annotations

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers import health


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: open pools, warm caches, validate config.
    yield
    # Shutdown: close clients.


def create_app() -> FastAPI:
    app = FastAPI(
        title=os.getenv("APP_NAME", "Healthcare Analytics Platform"),
        version="0.1.0",
        lifespan=lifespan,
    )
    app.include_router(health.router, tags=["health"])
    return app


app = create_app()
