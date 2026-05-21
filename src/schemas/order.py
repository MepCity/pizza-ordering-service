from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field


class OrderStatus(str, Enum):
    preparing = "preparing"
    ready = "ready"
    delivered = "delivered"


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(ge=1, le=20)
    extras: list[str] = Field(default_factory=list)


class OrderCreateRequest(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderStatusUpdateRequest(BaseModel):
    status: OrderStatus


class CouponApplyRequest(BaseModel):
    coupon_code: str = Field(min_length=3, max_length=50)


class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    extras: list[str]
    unit_price: Decimal
    line_total: Decimal

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    customer_name: str
    status: str
    subtotal: Decimal
    discount_amount: Decimal
    total_price: Decimal
    coupon_code: str | None
    created_at: datetime
    items: list[OrderItemResponse]

    model_config = {"from_attributes": True}


class OrderSummaryResponse(BaseModel):
    id: int
    customer_name: str
    status: str
    total_price: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}
