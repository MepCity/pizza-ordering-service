from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Pizza Ordering Service"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./pizza.db"
    s3_archive_enabled: bool = False
    s3_bucket_name: str = "pizza-orders"
    aws_region: str = "us-east-1"
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    aws_endpoint_url: str = "http://localhost:4566"
    otel_enabled: bool = False
    otel_service_name: str = "pizza-ordering-service"
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    otel_exporter_otlp_insecure: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
