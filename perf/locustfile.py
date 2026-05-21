from locust import HttpUser, between, task


class PizzaOrderingUser(HttpUser):
    wait_time = between(1, 2)

    @task(2)
    def list_menu(self) -> None:
        self.client.get("/menu")

    @task(3)
    def create_and_update_order(self) -> None:
        create_response = self.client.post(
            "/orders",
            json={
                "customer_name": "Locust User",
                "items": [
                    {
                        "menu_item_id": 1,
                        "quantity": 1,
                        "extras": ["olive"],
                    }
                ],
            },
        )
        if not create_response.ok:
            return

        order_id = create_response.json()["id"]
        self.client.patch(f"/orders/{order_id}/status", json={"status": "preparing"})
