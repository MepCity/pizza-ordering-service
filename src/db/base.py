from sqlalchemy.orm import DeclarativeBase


# Tüm veritabanı modellerinin miras aldığı temel sınıf
class Base(DeclarativeBase):
    pass
