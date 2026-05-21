from decimal import Decimal

from pydantic import BaseModel


class MenuItemResponse(BaseModel):
    id: int
    name: str
    size: str
    base_price: Decimal
    is_available: bool

    model_config = {"from_attributes": True}
