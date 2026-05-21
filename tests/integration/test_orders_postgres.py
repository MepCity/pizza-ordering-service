import json

from fastapi.testclient import TestClient


def test_create_order_persists_to_postgres(postgres_test_client: TestClient) -> None:
    response = postgres_test_client.post(
        "/orders",
        json={
            "customer_name": "Integration User",
            "items": [
                {
                    "menu_item_id": 1,
                    "quantity": 2,
                    "extras": ["olive", "jalapeno"],
                }
            ],
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["customer_name"] == "Integration User"
    assert body["status"] == "pending"
    assert body["items"][0]["quantity"] == 2
    assert body["items"][0]["extras"] == ["olive", "jalapeno"]
    assert body["subtotal"] == "27.98"
    assert body["total_price"] == "27.98"


def test_apply_coupon_updates_persisted_totals(postgres_test_client: TestClient) -> None:
    create_response = postgres_test_client.post(
        "/orders",
        json={
            "customer_name": "Coupon Integration User",
            "items": [{"menu_item_id": 2, "quantity": 1, "extras": ["mushroom"]}],
        },
    )
    order_id = create_response.json()["id"]

    coupon_response = postgres_test_client.post(
        f"/orders/{order_id}/apply-coupon",
        json={"coupon_code": "PIZZA10"},
    )
    fetch_response = postgres_test_client.get(f"/orders/{order_id}")

    assert coupon_response.status_code == 200
    coupon_body = coupon_response.json()
    assert coupon_body["coupon_code"] == "PIZZA10"
    assert coupon_body["discount_amount"] == "1.45"
    assert coupon_body["total_price"] == "13.04"

    assert fetch_response.status_code == 200
    fetch_body = fetch_response.json()
    assert fetch_body["coupon_code"] == "PIZZA10"
    assert fetch_body["discount_amount"] == "1.45"
    assert fetch_body["total_price"] == "13.04"


def test_create_order_archives_summary_to_localstack_s3(
    postgres_test_client: TestClient, localstack_s3
) -> None:
    response = postgres_test_client.post(
        "/orders",
        json={
            "customer_name": "Archive Integration User",
            "items": [{"menu_item_id": 1, "quantity": 1, "extras": ["olive"]}],
        },
    )

    assert response.status_code == 201
    order_id = response.json()["id"]

    s3_client = localstack_s3.get_client("s3")
    s3_object = s3_client.get_object(
        Bucket="pizza-orders-test",
        Key=f"orders/{order_id}.json",
    )
    payload = json.loads(s3_object["Body"].read().decode("utf-8"))

    assert payload["order_id"] == order_id
    assert payload["customer_name"] == "Archive Integration User"
    assert payload["items"][0]["extras"] == ["olive"]
