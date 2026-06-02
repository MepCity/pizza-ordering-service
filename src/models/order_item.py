from decimal import Decimal

from sqlalchemy import JSON, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base


# order_items tablosu — bir siparişin içindeki her pizza kalemi ayrı satır
class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)       # hangi siparişe ait
    menu_item_id: Mapped[int] = mapped_column(ForeignKey("menu_items.id"), nullable=False)# hangi pizza
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    extras: Mapped[list[str]] = mapped_column(JSON, default=list, nullable=False)         # ek malzemeler JSON olarak saklanır
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)           # birim fiyat (sipariş anındaki)
    line_total: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)           # quantity × unit_price + extras

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")
