from datetime import datetime, timezone
from decimal import Decimal

import factory
from faker import Faker

from src.models import MenuItem, Order, OrderItem

fake = Faker()


class MenuItemFactory(factory.Factory):
    class Meta:
        model = MenuItem

    id = factory.Sequence(lambda n: n + 1)
    name = factory.Iterator(["Margherita", "Pepperoni", "Vegetarian"])
    size = factory.Iterator(["small", "medium", "large"])
    base_price = factory.LazyFunction(
        lambda: Decimal(
            fake.pydecimal(left_digits=2, right_digits=2, positive=True)
        )
    )
    is_available = True


class OrderItemFactory(factory.Factory):
    class Meta:
        model = OrderItem

    id = factory.Sequence(lambda n: n + 1)
    menu_item_id = 1
    quantity = factory.Faker("random_int", min=1, max=3)
    extras = factory.LazyFunction(lambda: ["olive"])
    unit_price = Decimal("8.99")
    line_total = Decimal("11.49")


class OrderFactory(factory.Factory):
    class Meta:
        model = Order

    id = factory.Sequence(lambda n: n + 1)
    customer_name = factory.Faker("name")
    status = "pending"
    subtotal = Decimal("11.49")
    discount_amount = Decimal("0.00")
    total_price = Decimal("11.49")
    coupon_code = None
    created_at = factory.LazyFunction(lambda: datetime.now(timezone.utc))
    items = factory.LazyFunction(lambda: [OrderItemFactory()])
