from fastapi import FastAPI

from app.api import router


def create_app() -> FastAPI:
    app = FastAPI(title="Creative Director OS API", version="0.1.0")
    app.include_router(router)
    return app


app = create_app()
