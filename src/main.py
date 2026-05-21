from contextlib import asynccontextmanager

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from src.api.routes import router
from src.db.base import Base
from src.db.init_db import seed_menu_items
from src.db.session import SessionLocal, engine
from src.schemas.config import get_settings

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_menu_items(db)
    finally:
        db.close()
    yield


app = FastAPI(title=settings.app_name, version=settings.app_version, lifespan=lifespan)
app.include_router(router)
Instrumentator().instrument(app).expose(app)


@app.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
