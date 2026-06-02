from datetime import datetime
from decimal import Decimal
from enum import Enum

from pydantic import BaseModel, Field, field_validator

from src.services.pricing import SUPPORTED_EXTRAS


# Durum güncellemede kullanılabilecek geçerli değerler (pending hariç — başlangıç durumu)
class OrderStatus(str, Enum):
    preparing = "preparing"
    ready = "ready"
    delivered = "delivered"


# Sipariş kaleminin giriş şeması — kullanıcıdan gelen veriyi doğrular
class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int = Field(ge=1, le=20)  # en az 1, en fazla 20
    extras: list[str] = Field(default_factory=list)

    # Gelen extra listesini küçük harfe çevirir, geçersiz varsa hata fırlatır
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


# POST /orders body'si — müşteri adı ve en az 1 kalem zorunlu
class OrderCreateRequest(BaseModel):
    customer_name: str = Field(min_length=2, max_length=100)
    items: list[OrderItemCreate] = Field(min_length=1)


# PATCH /orders/{id}/status body'si
class OrderStatusUpdateRequest(BaseModel):
    status: OrderStatus


# POST /orders/{id}/apply-coupon body'si
class CouponApplyRequest(BaseModel):
    coupon_code: str = Field(min_length=3, max_length=50)


# API'den dönen sipariş kalemi — DB modelinden okur (from_attributes)
class OrderItemResponse(BaseModel):
    id: int
    menu_item_id: int
    quantity: int
    extras: list[str]
    unit_price: Decimal
    line_total: Decimal

    model_config = {"from_attributes": True}


# API'den dönen tam sipariş detayı
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


# GET /orders listesinde dönen özet — gereksiz alanlar yok
class OrderSummaryResponse(BaseModel):
    id: int
    customer_name: str
    status: str
    total_price: Decimal
    created_at: datetime

    model_config = {"from_attributes": True}
