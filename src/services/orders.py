from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload

from src.models import MenuItem, Order, OrderItem
from src.schemas.order import CouponApplyRequest, OrderCreateRequest
from src.services.pricing import calculate_discount, calculate_line_total

VALID_STATUS_TRANSITIONS = {
    "pending": {"preparing"},
    "preparing": {"ready"},
    "ready": {"delivered"},
    "delivered": set(),
}


def list_menu_items(db: Session) -> list[MenuItem]:
    return db.query(MenuItem).filter(MenuItem.is_available.is_(True)).order_by(MenuItem.id).all()


def list_orders(db: Session) -> list[Order]:
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .order_by(Order.created_at.desc())
        .all()
    )


def get_order_by_id(db: Session, order_id: int) -> Order:
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id)
        .first()
    )
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    return order


def create_order(db: Session, payload: OrderCreateRequest) -> Order:
    menu_item_ids = [item.menu_item_id for item in payload.items]
    menu_items = (
        db.query(MenuItem)
        .filter(MenuItem.id.in_(menu_item_ids), MenuItem.is_available.is_(True))
        .all()
    )
    menu_item_map = {item.id: item for item in menu_items}

    if len(menu_item_map) != len(set(menu_item_ids)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="One or more menu items are invalid or unavailable",
        )

    order_items: list[OrderItem] = []
    subtotal = Decimal("0.00")

    for item in payload.items:
        menu_item = menu_item_map[item.menu_item_id]
        unit_price = Decimal(str(menu_item.base_price))
        line_total = calculate_line_total(unit_price, item.quantity, len(item.extras))
        subtotal += line_total
        order_items.append(
            OrderItem(
                menu_item_id=menu_item.id,
                quantity=item.quantity,
                extras=item.extras,
                unit_price=unit_price,
                line_total=line_total,
            )
        )

    order = Order(
        customer_name=payload.customer_name,
        status="pending",
        subtotal=subtotal.quantize(Decimal("0.01")),
        discount_amount=Decimal("0.00"),
        total_price=subtotal.quantize(Decimal("0.01")),
        items=order_items,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return get_order_by_id(db, order.id)


def update_order_status(db: Session, order_id: int, new_status: str) -> Order:
    order = get_order_by_id(db, order_id)
    normalized_status = str(new_status).lower()

    allowed_transitions = VALID_STATUS_TRANSITIONS.get(order.status, set())
    if normalized_status not in allowed_transitions:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status transition from {order.status} to {normalized_status}",
        )

    order.status = normalized_status
    db.commit()
    db.refresh(order)
    return get_order_by_id(db, order.id)


def apply_coupon(db: Session, order_id: int, payload: CouponApplyRequest) -> Order:
    order = get_order_by_id(db, order_id)

    if order.coupon_code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A coupon has already been applied to this order",
        )

    try:
        discount_amount = calculate_discount(order.subtotal, payload.coupon_code)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    order.coupon_code = payload.coupon_code.upper()
    order.discount_amount = discount_amount
    order.total_price = (order.subtotal - discount_amount).quantize(Decimal("0.01"))
    db.commit()
    db.refresh(order)
    return get_order_by_id(db, order.id)
