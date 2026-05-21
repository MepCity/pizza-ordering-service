from decimal import Decimal

EXTRA_PRICE = Decimal("2.50")
SUPPORTED_EXTRAS = {
    "extra_cheese",
    "jalapeno",
    "mushroom",
    "olive",
    "pepperoni",
}
SUPPORTED_COUPONS = {
    "PIZZA10": Decimal("0.10"),
    "CHEESE20": Decimal("0.20"),
}


def calculate_line_total(unit_price: Decimal, quantity: int, extras_count: int) -> Decimal:
    extras_total = EXTRA_PRICE * extras_count * quantity
    return (unit_price * quantity) + extras_total


def calculate_discount(subtotal: Decimal, coupon_code: str | None) -> Decimal:
    if not coupon_code:
        return Decimal("0.00")

    rate = SUPPORTED_COUPONS.get(coupon_code.upper())
    if rate is None:
        raise ValueError("Invalid coupon code")

    return (subtotal * rate).quantize(Decimal("0.01"))
