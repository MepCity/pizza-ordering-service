from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.session import get_db
from src.schemas.menu import MenuItemResponse
from src.schemas.order import (
    CouponApplyRequest,
    OrderCreateRequest,
    OrderResponse,
    OrderStatusUpdateRequest,
    OrderSummaryResponse,
)
from src.services.orders import (
    apply_coupon,
    create_order,
    get_order_by_id,
    list_menu_items,
    list_orders,
    update_order_status,
)

router = APIRouter()


@router.get("/menu", response_model=list[MenuItemResponse])
def get_menu(db: Session = Depends(get_db)) -> list[MenuItemResponse]:
    return list_menu_items(db)


@router.post("/orders", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_new_order(
    payload: OrderCreateRequest, db: Session = Depends(get_db)
) -> OrderResponse:
    return create_order(db, payload)


@router.get("/orders", response_model=list[OrderSummaryResponse])
def get_orders(db: Session = Depends(get_db)) -> list[OrderSummaryResponse]:
    return list_orders(db)


@router.get("/orders/{order_id}", response_model=OrderResponse)
def get_order(order_id: int, db: Session = Depends(get_db)) -> OrderResponse:
    return get_order_by_id(db, order_id)


@router.patch("/orders/{order_id}/status", response_model=OrderResponse)
def patch_order_status(
    order_id: int, payload: OrderStatusUpdateRequest, db: Session = Depends(get_db)
) -> OrderResponse:
    return update_order_status(db, order_id, payload.status)


@router.post("/orders/{order_id}/apply-coupon", response_model=OrderResponse)
def apply_order_coupon(
    order_id: int, payload: CouponApplyRequest, db: Session = Depends(get_db)
) -> OrderResponse:
    return apply_coupon(db, order_id, payload)
