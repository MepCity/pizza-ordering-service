from fastapi import APIRouter, Depends, status
from fastapi.responses import HTMLResponse
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


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
def home() -> str:
    return """
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <title>Pizza Ordering Service</title>
        <style>
          body { font-family: sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }
          h1 { margin-bottom: 0.5rem; }
          form, section {
            border: 1px solid #ddd;
            border-radius: 12px;
            padding: 1rem;
            margin-top: 1rem;
          }
          label { display: block; margin-top: 0.75rem; }
          input, select, button { margin-top: 0.25rem; padding: 0.5rem; width: 100%; }
          button { cursor: pointer; }
          pre { background: #f6f6f6; padding: 1rem; border-radius: 8px; overflow-x: auto; }
        </style>
      </head>
      <body>
        <h1>Pizza Ordering Service</h1>
        <p id="menu-status">Loading menu...</p>
        <section>
          <h2>Create Order</h2>
          <form id="order-form">
            <label>
              Customer Name
              <input id="customer-name" name="customer-name" value="Web User" />
            </label>
            <label>
              Menu Item
              <select id="menu-item"></select>
            </label>
            <label>
              Quantity
              <input id="quantity" type="number" value="1" min="1" max="20" />
            </label>
            <label>
              Extras
              <input id="extras" value="olive" />
            </label>
            <button id="submit-order" type="submit">Create Order</button>
          </form>
        </section>
        <section>
          <h2>Latest Response</h2>
          <pre id="order-result">No order created yet.</pre>
        </section>
        <script>
          const menuStatus = document.getElementById("menu-status");
          const menuSelect = document.getElementById("menu-item");
          const orderForm = document.getElementById("order-form");
          const orderResult = document.getElementById("order-result");

          async function loadMenu() {
            const response = await fetch("/menu");
            const menu = await response.json();
            menu.forEach((item) => {
              const option = document.createElement("option");
              option.value = item.id;
              option.textContent = `${item.name} (${item.size}) - $${item.base_price}`;
              menuSelect.appendChild(option);
            });
            menuStatus.textContent = `Loaded ${menu.length} menu items`;
          }

          orderForm.addEventListener("submit", async (event) => {
            event.preventDefault();
            const extras = document.getElementById("extras").value
              .split(",")
              .map((value) => value.trim().toLowerCase())
              .filter(Boolean);

            const payload = {
              customer_name: document.getElementById("customer-name").value,
              items: [
                {
                  menu_item_id: Number(menuSelect.value),
                  quantity: Number(document.getElementById("quantity").value),
                  extras
                }
              ]
            };

            const response = await fetch("/orders", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(payload)
            });
            const body = await response.json();
            orderResult.textContent = JSON.stringify(body, null, 2);
          });

          loadMenu();
        </script>
      </body>
    </html>
    """


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
