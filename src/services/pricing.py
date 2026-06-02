from decimal import Decimal

# Her extra malzeme sabit 2.50 dolar
EXTRA_PRICE = Decimal("2.50")

# Geçerli extra malzemeler — başka bir şey gelirse kabul edilmez
SUPPORTED_EXTRAS = {
    "extra_cheese",
    "jalapeno",
    "mushroom",
    "olive",
    "pepperoni",
}

# Geçerli kupon kodları ve indirim oranları
SUPPORTED_COUPONS = {
    "PIZZA10": Decimal("0.10"),   # %10 indirim
    "CHEESE20": Decimal("0.20"),  # %20 indirim
}


# Bir sipariş kaleminin toplam fiyatını hesaplar: (birim fiyat × adet) + (extra × adet)
def calculate_line_total(unit_price: Decimal, quantity: int, extras_count: int) -> Decimal:
    extras_total = EXTRA_PRICE * extras_count * quantity
    return (unit_price * quantity) + extras_total


# Kupon koduna göre indirim tutarını döndürür, geçersiz kodda hata fırlatır
def calculate_discount(subtotal: Decimal, coupon_code: str | None) -> Decimal:
    if not coupon_code:
        return Decimal("0.00")

    rate = SUPPORTED_COUPONS.get(coupon_code.upper())
    if rate is None:
        raise ValueError("Invalid coupon code")

    return (subtotal * rate).quantize(Decimal("0.01"))
