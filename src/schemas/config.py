from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


# Tüm ortam değişkenlerini tek yerden yönetir — .env dosyasından veya sistem env'den okur
class Settings(BaseSettings):
    app_name: str = "Pizza Ordering Service"
    app_version: str = "0.1.0"
    database_url: str = "sqlite:///./pizza.db"   # Docker'da PostgreSQL, lokalde SQLite
    s3_archive_enabled: bool = False              # True ise siparişler S3'e arşivlenir
    s3_bucket_name: str = "pizza-orders"
    aws_region: str = "us-east-1"
    aws_access_key_id: str = "test"
    aws_secret_access_key: str = "test"
    aws_endpoint_url: str = "http://localhost:4566"  # LocalStack adresi
    otel_enabled: bool = False                    # True ise Jaeger'a trace gönderilir
    otel_service_name: str = "pizza-ordering-service"
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"
    otel_exporter_otlp_insecure: bool = True

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# lru_cache: Settings objesi bir kez oluşturulur, her çağrıda aynısı döner
@lru_cache
def get_settings() -> Settings:
    return Settings()
