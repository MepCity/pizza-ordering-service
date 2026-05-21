from fastapi.testclient import TestClient

from src.schemas.config import get_settings
from src.services import orders as order_service


def test_get_menu_returns_seeded_items(test_client: TestClient) -> None:
    response = test_client.get("/menu")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) >= 6
    assert payload[0]["name"] == "Margherita"


def test_create_order_returns_created_order(test_client: TestClient) -> None:
    payload = {
        "customer_name": "Yasir",
        "items": [
            {
                "menu_item_id": 1,
                "quantity": 2,
                "extras": ["jalapeno", "mushroom"],
            }
        ],
    }

    response = test_client.post("/orders", json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["customer_name"] == "Yasir"
    assert body["status"] == "pending"
    assert body["items"][0]["quantity"] == 2
    assert body["items"][0]["extras"] == ["jalapeno", "mushroom"]


def test_create_order_rejects_unsupported_extra(test_client: TestClient) -> None:
    response = test_client.post(
        "/orders",
        json={
            "customer_name": "Invalid Extra User",
            "items": [
                {
                    "menu_item_id": 1,
                    "quantity": 1,
                    "extras": ["pineapple"],
                }
            ],
        },
    )

    assert response.status_code == 422
    assert "Unsupported extras" in response.text


def test_apply_coupon_cannot_be_used_twice(test_client: TestClient) -> None:
    create_response = test_client.post(
        "/orders",
        json={
            "customer_name": "Coupon User",
            "items": [{"menu_item_id": 2, "quantity": 1, "extras": []}],
        },
    )
    order_id = create_response.json()["id"]

    first_response = test_client.post(
        f"/orders/{order_id}/apply-coupon",
        json={"coupon_code": "PIZZA10"},
    )
    second_response = test_client.post(
        f"/orders/{order_id}/apply-coupon",
        json={"coupon_code": "CHEESE20"},
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "A coupon has already been applied to this order"


def test_apply_coupon_rejects_unknown_code(test_client: TestClient) -> None:
    create_response = test_client.post(
        "/orders",
        json={
            "customer_name": "Invalid Coupon User",
            "items": [{"menu_item_id": 2, "quantity": 1, "extras": []}],
        },
    )
    order_id = create_response.json()["id"]

    response = test_client.post(
        f"/orders/{order_id}/apply-coupon",
        json={"coupon_code": "INVALID50"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Invalid coupon code"


def test_invalid_status_transition_returns_bad_request(test_client: TestClient) -> None:
    create_response = test_client.post(
        "/orders",
        json={
            "customer_name": "Status User",
            "items": [{"menu_item_id": 3, "quantity": 1, "extras": []}],
        },
    )
    order_id = create_response.json()["id"]

    response = test_client.patch(
        f"/orders/{order_id}/status",
        json={"status": "delivered"},
    )

    assert response.status_code == 400
    assert "Invalid status transition" in response.json()["detail"]


def test_order_status_can_progress_sequentially(test_client: TestClient) -> None:
    create_response = test_client.post(
        "/orders",
        json={
            "customer_name": "Flow User",
            "items": [{"menu_item_id": 3, "quantity": 1, "extras": []}],
        },
    )
    order_id = create_response.json()["id"]

    preparing_response = test_client.patch(
        f"/orders/{order_id}/status",
        json={"status": "preparing"},
    )
    ready_response = test_client.patch(
        f"/orders/{order_id}/status",
        json={"status": "ready"},
    )
    delivered_response = test_client.patch(
        f"/orders/{order_id}/status",
        json={"status": "delivered"},
    )

    assert preparing_response.status_code == 200
    assert preparing_response.json()["status"] == "preparing"
    assert ready_response.status_code == 200
    assert ready_response.json()["status"] == "ready"
    assert delivered_response.status_code == 200
    assert delivered_response.json()["status"] == "delivered"


def test_create_order_archives_to_s3_when_enabled(
    monkeypatch, test_client: TestClient
) -> None:
    settings = get_settings()
    original_flag = settings.s3_archive_enabled
    captured: dict[str, int] = {}

    def fake_archive(order):
        captured["order_id"] = order.id

    monkeypatch.setattr(order_service, "archive_order_summary", fake_archive)
    settings.s3_archive_enabled = True

    response = test_client.post(
        "/orders",
        json={
            "customer_name": "Archive Flow User",
            "items": [{"menu_item_id": 1, "quantity": 1, "extras": ["olive"]}],
        },
    )

    settings.s3_archive_enabled = original_flag

    assert response.status_code == 201
    assert captured["order_id"] == response.json()["id"]
