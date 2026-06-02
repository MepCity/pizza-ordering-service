from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from src.schemas.config import get_settings

settings = get_settings()

# Veritabanı bağlantı motoru — DATABASE_URL env'den gelir (SQLite veya PostgreSQL)
engine = create_engine(settings.database_url, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


# Her API isteği için ayrı bir DB oturumu açar, istek bitince kapatır
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
