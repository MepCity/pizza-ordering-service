from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from src.services.pricing import SUPPORTED_EXTRAS


class OrderStatus(str, Enum):
    preparing = "preparing"
    ready = "ready"
    delivered = "delivered"


class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(ge=1, le=20)
    extras: list[str] = Field(default_factory=list)

    @field_validator("extras")
    @classmethod
    def validate_extras(cls, extras: list[str]) -> list[str]:
        normalized_extras = [extra.strip().lower() for extra in extras]
        invalid_extras = [extra for extra in normalized_extras if extra not in SUPPORTED_EXTRAS]
        if invalid_extras:
            supported_extras = ", ".join(sorted(SUPPORTED_EXTRAS))
            invalid_list = ", ".join(invalid_extras)
            raise ValueError(
                f"Unsupported extras: {invalid_list}. Supported extras: {supported_extras}"
            )
        return normalized_extras


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
