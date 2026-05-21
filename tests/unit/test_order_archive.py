from datetime import datetime, timezone
from decimal import Decimal

from src.integrations.order_archive import build_order_summary
from src.models import Order, OrderItem


def test_build_order_summary_serializes_order_fields() -> None:
    order = Order(
        id=42,
        customer_name="Archive User",
        status="pending",
        subtotal=Decimal("17.99"),
        discount_amount=Decimal("2.00"),
        total_price=Decimal("15.99"),
        coupon_code="PIZZA10",
        created_at=datetime(2026, 5, 21, 12, 0, tzinfo=timezone.utc),
    )
    order.items = [
        OrderItem(
            menu_item_id=1,
            quantity=2,
            extras=["jalapeno", "olive"],
            unit_price=Decimal("8.99"),
            line_total=Decimal("22.98"),
        )
    ]

    summary = build_order_summary(order)

    assert summary["order_id"] == 42
    assert summary["subtotal"] == "17.99"
    assert summary["discount_amount"] == "2.00"
    assert summary["total_price"] == "15.99"
    assert summary["items"][0]["extras"] == ["jalapeno", "olive"]
    assert summary["items"][0]["unit_price"] == "8.99"
