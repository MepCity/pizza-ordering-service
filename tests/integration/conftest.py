from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from testcontainers.localstack import LocalStackContainer
from testcontainers.postgres import PostgresContainer

from src.db.base import Base
from src.db.init_db import seed_menu_items
from src.db.session import get_db
from src.main import app
from src.schemas.config import get_settings


@pytest.fixture
def postgres_test_client() -> Generator[TestClient, None, None]:
    try:
        container = PostgresContainer("postgres:16")
        container.start()
    except Exception as exc:
        pytest.skip(f"PostgreSQL test container could not be started: {exc}")

    engine = create_engine(container.get_connection_url(driver="psycopg"), future=True)
    testing_session_local = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    Base.metadata.create_all(bind=engine)

    db = testing_session_local()
    try:
        seed_menu_items(db)
    finally:
        db.close()

    def override_get_db() -> Generator[Session, None, None]:
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)
    engine.dispose()
    container.stop()


@pytest.fixture
def localstack_s3() -> Generator[LocalStackContainer, None, None]:
    settings = get_settings()
    original_flag = settings.s3_archive_enabled
    original_endpoint = settings.aws_endpoint_url
    original_region = settings.aws_region
    original_access_key = settings.aws_access_key_id
    original_secret_key = settings.aws_secret_access_key
    original_bucket_name = settings.s3_bucket_name

    try:
        container = LocalStackContainer(image="localstack/localstack:3.5").with_services("s3")
        container.start()
    except Exception as exc:
        pytest.skip(f"LocalStack test container could not be started: {exc}")

    settings.s3_archive_enabled = True
    settings.aws_endpoint_url = container.get_url()
    settings.aws_region = container.region_name
    settings.aws_access_key_id = "testcontainers-localstack"
    settings.aws_secret_access_key = "testcontainers-localstack"
    settings.s3_bucket_name = "pizza-orders-test"

    yield container

    settings.s3_archive_enabled = original_flag
    settings.aws_endpoint_url = original_endpoint
    settings.aws_region = original_region
    settings.aws_access_key_id = original_access_key
    settings.aws_secret_access_key = original_secret_key
    settings.s3_bucket_name = original_bucket_name
    container.stop()
