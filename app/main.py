from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import admin_users, auth, users
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title="School Auth")

    if settings.cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(auth.router)
    app.include_router(users.router)
    app.include_router(admin_users.router)
    return app


app = create_app()

__all__ = ["app"]
