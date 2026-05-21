from fastapi.testclient import TestClient


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
