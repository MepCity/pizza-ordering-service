from decimal import Decimal

from sqlalchemy import Boolean, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.base import Base


# menu_items tablosu — her satır bir pizza çeşidi ve boyutunu temsil eder
class MenuItem(Base):
    __tablename__ = "menu_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    # small / medium / large
    size: Mapped[str] = mapped_column(String(20), nullable=False)
    base_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    # False ise menude gosterilmez
    is_available: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
