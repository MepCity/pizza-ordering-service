from decimal import Decimal

from src.integrations.order_archive import build_order_summary
from tests.factories import OrderFactory, OrderItemFactory


def test_build_order_summary_serializes_order_fields() -> None:
    order = OrderFactory(
        id=42,
        coupon_code="PIZZA10",
        subtotal=Decimal("17.99"),
        discount_amount=Decimal("2.00"),
        total_price=Decimal("15.99"),
    )
    order.items = [OrderItemFactory(menu_item_id=1, quantity=2, extras=["jalapeno", "olive"])]

    summary = build_order_summary(order)

    assert summary["order_id"] == 42
    assert summary["subtotal"] == "17.99"
    assert summary["discount_amount"] == "2.00"
    assert summary["total_price"] == "15.99"
    assert summary["items"][0]["extras"] == ["jalapeno", "olive"]
    assert summary["items"][0]["unit_price"] == "8.99"
